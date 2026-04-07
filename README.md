# MedEdge 🏥

**AI-Powered Triage Assistant for Community Health Workers**

> Built for the [Gemma 4 Good Hackathon](https://www.kaggle.com/competitions/gemma-4-good-hackathon) · Health & Sciences Track

MedEdge puts the power of Gemma 4 in the hands of community health workers in remote, resource-limited settings — clinics with no specialists, disaster zones with no connectivity, villages hours from the nearest hospital.

A health worker photographs a patient's condition. MedEdge analyzes it, queries an offline WHO/MSF protocol database, and returns a structured triage decision in seconds — in the health worker's own language.

---

## Demo

**[Live Demo →](https://your-demo-url)**

![MedEdge Screenshot](docs/screenshot.png)

---

## How It Works

```
Health Worker
     │
     ▼
 Photo + Symptoms
     │
     ▼
┌─────────────────────────────────────────┐
│            Gemma 4 Agent                │
│                                         │
│  1. Analyze image (multimodal)          │
│  2. → search_medical_protocols()        │
│     (ChromaDB · offline · WHO/MSF)      │
│  3. → assess_vital_signs()  (if given)  │
│  4. → get_referral_guidance()           │
│  5. Synthesize triage report            │
└─────────────────────────────────────────┘
     │
     ▼
 RED / YELLOW / GREEN
 + Immediate Actions
 + Red Flags
 + Referral Guidance
 + 9 Languages
```

### Key Gemma 4 Features Used

| Feature | How MedEdge Uses It |
|---|---|
| **Multimodal understanding** | Analyzes wound/rash/burn photos directly |
| **Native function calling** | Agent decides when to query protocols, assess vitals, get referral guidance |
| **Agentic loop** | Multi-turn reasoning before producing final triage |
| **Edge-ready** | Architecture designed for local deployment via Ollama |

---

## Tracks

- **Main Track** — Best overall project
- **Health & Sciences** — Tools that democratize medical knowledge
- **Digital Equity & Inclusivity** — 9 languages including Swahili, Arabic, Hausa, Amharic

---

## Stack

- **Model**: Gemma 4 (`gemma-4-31b-it`) via Google AI Studio
- **Function Calling**: 3 tools — `search_medical_protocols`, `assess_vital_signs`, `get_referral_guidance`
- **Offline Protocol DB**: ChromaDB + sentence-transformers (WHO/MSF guidelines)
- **Backend**: FastAPI + Server-Sent Events (streaming)
- **Frontend**: Vanilla JS, mobile-first, no framework

---

## Setup

### 1. Clone & install

```bash
git clone https://github.com/YOUR_USERNAME/medge.git
cd medge
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Set API key

```bash
export GOOGLE_API_KEY="your-google-ai-studio-key"
```

Get a free key at [aistudio.google.com](https://aistudio.google.com).

### 3. Run

```bash
./scripts/start.sh
```

Open `http://localhost:8000`

---

## Project Structure

```
medge/
├── backend/
│   ├── main.py        # FastAPI app, SSE streaming endpoint
│   ├── triage.py      # Gemma 4 agentic loop + function calling
│   ├── tools.py       # Tool implementations (protocols, vitals, referral)
│   └── db.py          # ChromaDB vector store
├── data/
│   └── protocols.py   # WHO/MSF protocol seed data (8 categories)
├── frontend/
│   └── index.html     # Mobile-first UI with live agentic panel
└── scripts/
    └── start.sh       # One-command launcher
```

---

## Supported Languages

English · French · Swahili · Arabic · Portuguese · Spanish · Hausa · Amharic · Hindi

---

## Offline Architecture

MedEdge is designed to run fully offline on a clinic's local server:

- **Protocol DB**: ChromaDB stores WHO/MSF guidelines locally
- **Inference**: Swap `GOOGLE_API_KEY` for local Ollama endpoint
- **No cloud dependency** in the production architecture

For the hackathon demo, inference runs via Google AI Studio API.

---

## License

Apache 2.0
