"""
Triage engine using Gemma 4 native function calling + agentic loop.
Gemma 4 decides which tools to call, in what order, and when it has enough
information to produce a final triage assessment.
"""

import base64
import json
import os
from typing import Generator

from google import genai
from google.genai import types

from backend.tools import search_medical_protocols, assess_vital_signs, get_referral_guidance

MODEL = "gemma-4-31b-it"

SYSTEM_PROMPT = """You are MedEdge, an AI triage assistant for community health workers in remote, resource-limited settings with no internet access.

You have access to the following tools:
- search_medical_protocols: Search the local offline WHO/MSF clinical protocol database
- assess_vital_signs: Evaluate patient vital signs for clinical risk
- get_referral_guidance: Get transfer and referral instructions for a given urgency level

WORKFLOW:
1. Analyze the patient photo carefully for visible signs
2. Call search_medical_protocols to retrieve relevant clinical guidelines
3. If vitals are mentioned, call assess_vital_signs
4. Based on your assessment, call get_referral_guidance with the appropriate urgency (RED/YELLOW/GREEN)
5. Synthesize everything into a structured final report

OUTPUT FORMAT (always end with this structure):
### Assessment
[What you see in the image + clinical interpretation]

### Triage Level: [RED/YELLOW/GREEN]
[One sentence justification]

### Immediate Actions
[Numbered list of what the health worker should do right now]

### Red Flags to Watch
[Bullet list of signs that should trigger urgent referral]

### When to Refer
[Specific referral instructions]

Keep language simple — the health worker may not be a trained clinician.
Always remind: this is decision support, not diagnosis. When in doubt, refer."""


FUNCTION_DECLARATIONS = [
    types.FunctionDeclaration(
        name="search_medical_protocols",
        description="Search the local offline medical protocol database for WHO/MSF clinical guidelines relevant to the patient's condition. Call this first with a description of what you see.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "query": types.Schema(
                    type=types.Type.STRING,
                    description="Description of the condition or symptom to search for",
                ),
                "category": types.Schema(
                    type=types.Type.STRING,
                    description="Optional category filter",
                    enum=["trauma", "infectious", "respiratory", "dermatology", "pediatric", "obstetric", "any"],
                ),
            },
            required=["query"],
        ),
    ),
    types.FunctionDeclaration(
        name="assess_vital_signs",
        description="Evaluate patient vital signs for clinical risk. Call this if the health worker has reported any vital measurements.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "heart_rate": types.Schema(type=types.Type.NUMBER, description="Heart rate in bpm (optional)"),
                "respiratory_rate": types.Schema(type=types.Type.NUMBER, description="Breaths per minute (optional)"),
                "temperature_c": types.Schema(type=types.Type.NUMBER, description="Temperature in Celsius (optional)"),
                "spo2": types.Schema(type=types.Type.NUMBER, description="Oxygen saturation percentage (optional)"),
                "systolic_bp": types.Schema(type=types.Type.NUMBER, description="Systolic blood pressure mmHg (optional)"),
            },
        ),
    ),
    types.FunctionDeclaration(
        name="get_referral_guidance",
        description="Get referral and patient transfer instructions. Call this after you have determined the triage level (RED, YELLOW, or GREEN).",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "urgency_level": types.Schema(
                    type=types.Type.STRING,
                    description="The triage level you have determined",
                    enum=["RED", "YELLOW", "GREEN"],
                ),
            },
            required=["urgency_level"],
        ),
    ),
]

TOOL_MAP = {
    "search_medical_protocols": search_medical_protocols,
    "assess_vital_signs": assess_vital_signs,
    "get_referral_guidance": get_referral_guidance,
}


def _execute_tool(name: str, args: dict) -> str:
    fn = TOOL_MAP.get(name)
    if not fn:
        return json.dumps({"error": f"Unknown tool: {name}"})
    try:
        result = fn(**args)
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})


def run_triage_stream(
    image_bytes: bytes,
    mime_type: str,
    symptoms: str,
    patient_info: str = "",
    language: str = "English",
) -> Generator[dict, None, None]:
    """
    Agentic triage loop with native function calling.
    Yields SSE-style event dicts as the agent reasons through the case.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        yield {"type": "error", "message": "GOOGLE_API_KEY not set."}
        return

    client = genai.Client(api_key=api_key)

    system = SYSTEM_PROMPT
    if language.lower() != "english":
        system += f"\n\nIMPORTANT: Respond entirely in {language}."

    user_text = (
        f"Patient: {patient_info or 'Not provided'}\n"
        f"Symptoms: {symptoms}\n\n"
        "Please assess this patient using your tools, then provide the full triage report."
    )

    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    text_part = types.Part.from_text(text=user_text)

    messages = [
        types.Content(role="user", parts=[image_part, text_part])
    ]

    config = types.GenerateContentConfig(
        system_instruction=system,
        temperature=0.2,
        max_output_tokens=2048,
        tools=[types.Tool(function_declarations=FUNCTION_DECLARATIONS)],
    )

    tools_called = []
    final_text = ""
    max_turns = 6

    for turn in range(max_turns):
        response = client.models.generate_content(
            model=MODEL,
            contents=messages,
            config=config,
        )

        candidate = response.candidates[0]
        messages.append(types.Content(role="model", parts=candidate.content.parts))

        # Check for function calls
        fn_calls = [p for p in candidate.content.parts if p.function_call]

        if fn_calls:
            tool_results = []
            for part in fn_calls:
                fc = part.function_call
                args = dict(fc.args) if fc.args else {}

                yield {
                    "type": "tool_call",
                    "name": fc.name,
                    "args": args,
                }

                result_str = _execute_tool(fc.name, args)
                result_data = json.loads(result_str)
                tools_called.append(fc.name)

                yield {
                    "type": "tool_result",
                    "name": fc.name,
                    "result": result_data,
                }

                tool_results.append(
                    types.Part.from_function_response(
                        name=fc.name,
                        response=result_data,
                    )
                )

            messages.append(types.Content(role="user", parts=tool_results))

        else:
            # No more function calls — this is the final answer
            text_parts = [p for p in candidate.content.parts if p.text]
            raw = "\n".join(p.text for p in text_parts).strip()
            # Strip any preamble before the structured report
            marker = "### Assessment"
            idx = raw.find(marker)
            final_text = raw[idx:].strip() if idx != -1 else raw
            break

    # Determine triage level
    upper = final_text.upper()
    if "TRIAGE LEVEL: RED" in upper or "**RED**" in upper:
        level = "RED"
    elif "TRIAGE LEVEL: GREEN" in upper or "**GREEN**" in upper:
        level = "GREEN"
    else:
        level = "YELLOW"

    yield {
        "type": "final",
        "triage_level": level,
        "assessment": final_text,
        "tools_used": list(dict.fromkeys(tools_called)),
    }
