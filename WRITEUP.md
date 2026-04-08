# MedEdge: AI-Powered Triage for Community Health Workers

**Subtitle:** Bringing Gemma 4's agentic intelligence to remote clinics where every minute counts

**Track:** Health & Sciences · Digital Equity & Inclusivity

**Live Demo:** https://medge.onrender.com/  
**Code:** https://github.com/mkk2026/medge  
**Video:** [YouTube Link]

---

## The Problem

In Sierra Leone, where I live and build, the doctor-to-patient ratio is roughly 1 per 25,000 people. Community health workers (CHWs) are the frontline of healthcare in rural areas — often the only medical contact a patient will have before reaching a hospital hours away. These workers are brave, dedicated, and undertrained. They make life-or-death triage decisions with minimal tools, no connectivity, and no specialist backup.

A CHW sees a deep wound on a farmer's arm. Is it infected? Should the patient be stabilized locally or referred immediately? What are the red flags to watch? Right now, the answer depends entirely on memory and experience. The wrong call costs time — and sometimes lives.

## The Solution

MedEdge is an AI-powered triage assistant that puts Gemma 4's multimodal, agentic intelligence directly in the hands of community health workers. A CHW photographs a patient's condition, describes the symptoms, and MedEdge returns a structured triage decision — RED (refer urgently), YELLOW (monitor closely), or GREEN (manage locally) — with immediate actions, red flags, and referral guidance.

The key insight: this is not a chatbot. MedEdge is an autonomous clinical reasoning agent. Gemma 4 analyzes the image, decides which tools to invoke, queries an offline WHO/MSF protocol database, evaluates vital signs, retrieves referral guidance, and synthesizes everything into a structured report. The health worker sees the agent's reasoning process in real time — building trust and understanding in every assessment.

## Architecture

MedEdge uses three core Gemma 4 capabilities working together:

**Multimodal Understanding.** The patient photo is sent directly to Gemma 4 as a multimodal input. The model analyzes visible clinical signs — wound depth, burn severity, rash morphology, swelling — alongside the text description of symptoms.

**Native Function Calling.** Gemma 4 has access to three tools, declared as native function declarations:

- `search_medical_protocols()` — Queries a local ChromaDB vector store containing WHO Emergency Triage (ETAT+) and MSF Clinical Guidelines across 8 categories: trauma, burns, fever/infectious disease, respiratory distress, dermatology, dehydration, obstetric emergencies, and head injuries. The database uses sentence-transformers for semantic search, returning the most relevant protocol chunks for the patient's presentation.

- `assess_vital_signs()` — Evaluates any reported vital measurements (heart rate, respiratory rate, temperature, SpO2, blood pressure) against clinical thresholds derived from WHO guidelines, returning a risk level and specific flags.

- `get_referral_guidance()` — Returns structured transfer and referral instructions calibrated to the determined urgency level, including transport guidance, stabilization steps, and communication protocols.

**Agentic Loop.** Gemma 4 orchestrates these tools autonomously through a multi-turn reasoning loop (up to 6 turns). The model decides which tools to call, in what order, and when it has gathered enough information to produce a final assessment. This is not a fixed pipeline — the agent adapts its approach based on what it sees. A wound photo might trigger protocol search first; a case with reported vitals might trigger vital sign assessment before anything else.

The backend streams Server-Sent Events (SSE) to the frontend, so the health worker sees each tool call and result in real time through an "agentic thinking panel" — making the AI's reasoning transparent and explainable.

## Technical Stack

- **Model:** Gemma 4 (`gemma-4-31b-it`) via Google AI Studio API (demo); architecture supports local deployment via Ollama
- **Backend:** FastAPI with SSE streaming, Python
- **Vector Database:** ChromaDB with sentence-transformers embeddings, seeded with WHO/MSF protocols
- **Frontend:** Vanilla JavaScript, mobile-first, no framework dependencies — designed for low-bandwidth, low-powered devices
- **Deployment:** Render (demo); designed for offline clinic servers

## Offline-First Design

MedEdge is architected for environments where connectivity cannot be assumed. The protocol database runs entirely locally via ChromaDB. The frontend is a single HTML file with no CDN dependencies. For production deployment, inference can run locally by swapping the Google AI Studio endpoint for a local Ollama instance running Gemma 4 — no cloud dependency required. The hackathon demo uses the API for accessibility, but every architectural decision was made with offline deployment in mind.

## Multilingual Support

Healthcare delivery in sub-Saharan Africa crosses language boundaries constantly. MedEdge supports 9 languages: English, French, Swahili, Arabic, Portuguese, Spanish, Hausa, Amharic, and Hindi — covering the primary languages of health workers across Africa, South Asia, and Latin America. The language instruction is injected into the system prompt, and Gemma 4 generates the entire triage report in the selected language.

## Why Gemma 4

This project would not work the same way with a non-agentic model. The combination of multimodal input, native function calling, and multi-turn reasoning is what makes MedEdge a clinical reasoning agent rather than a simple classifier. Gemma 4's native function calling means the model decides its own workflow — it is not following a hardcoded pipeline. The open-weight nature of Gemma 4 is equally critical: deploying a closed API model in a clinic with no internet is impossible. Gemma 4's edge-ready design means MedEdge can actually run where it is needed.

## Challenges & Lessons

The biggest challenge was making the agentic loop reliable. Early iterations sometimes produced function calls with malformed arguments or entered loops without reaching a final assessment. Setting `temperature=0.2` and capping the loop at 6 turns solved both issues. Parsing the final triage level from the model's free-text output required a fallback heuristic — if the model doesn't explicitly state RED or GREEN, the system defaults to YELLOW (the safest clinical assumption).

Streaming SSE through Render's proxy required adding keepalive comments and disabling response buffering — a small but critical production detail.

## Impact

MedEdge addresses a real, urgent gap. Community health workers in Sierra Leone, the DRC, Chad, and dozens of other countries make triage decisions every day without decision support. MedEdge does not replace clinical judgment — it augments it. The structured output (triage level + immediate actions + red flags + referral guidance) maps directly to how CHW training programs already teach triage, making adoption natural.

The transparent reasoning panel is not just a UI feature — it is a teaching tool. A CHW using MedEdge learns why a wound is classified as RED, what vital sign thresholds matter, and which protocol applies. Over time, MedEdge builds clinical capacity, not just clinical output.

This is what Gemma 4 was built for: frontier intelligence, running locally, solving problems where they matter most.

---

*Built by Momodu Kamara-Kolleh · Core Brim Tech · Freetown, Sierra Leone*
