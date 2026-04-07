"""
MedEdge FastAPI backend — agentic triage with SSE streaming.
"""

import json
import os
import sys

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from backend.triage import run_triage_stream

app = FastAPI(title="MedEdge", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB

SUPPORTED_LANGUAGES = [
    "English", "French", "Swahili", "Arabic", "Portuguese",
    "Spanish", "Hausa", "Amharic", "Hindi",
]


@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.post("/api/triage")
async def triage(
    image: UploadFile = File(...),
    symptoms: str = Form(...),
    patient_info: str = Form(""),
    language: str = Form("English"),
):
    # Validate
    if image.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported image type: {image.content_type}.")

    symptoms = symptoms.strip()
    if not symptoms or len(symptoms) < 3:
        raise HTTPException(status_code=400, detail="Please describe the symptoms.")
    if len(symptoms) > 2000:
        raise HTTPException(status_code=400, detail="Symptoms too long (max 2000 chars).")

    if language not in SUPPORTED_LANGUAGES:
        language = "English"

    image_bytes = await image.read()
    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Image too large (max 10MB).")
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Empty image file.")

    patient_info = patient_info.strip()[:500]

    def event_stream():
        try:
            for event in run_triage_stream(
                image_bytes=image_bytes,
                mime_type=image.content_type,
                symptoms=symptoms,
                patient_info=patient_info,
                language=language,
            ):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/health")
async def health():
    return {"status": "ok", "model": "gemma-4-27b-it", "mode": "agentic-function-calling"}
