# CuraGennie — Voice-First AI Healthcare Assistant

> **"Your health deserves to be heard."**  
> Scaler × Wispr Flow Hackathon Project

CuraGennie is a production-grade, voice-first personal healthcare assistant designed for Indian families. It allows users to explain their health concerns naturally in **Hindi**, **Hinglish**, or **English**. The assistant asks a limited number of relevant follow-up questions, understands the reported symptoms, screens for acute emergency warning signs, explains non-diagnostic possible causes, and guides users to appropriate next steps, including verified doctors and tertiary hospital facilities.

It is a healthcare guidance and navigation product, **not** an autonomous diagnostic or prescription system.

---

## 🌟 Key Architecture & Capabilities

1. **Zero-Key Out-of-the-Box Guarantee**
   - Boots and runs 100% locally with zero external API keys required.
   - Deterministic clinical state machine, multilingual normalization dictionary, and emergency red-flag engine.
   - Optional LLM integration can be toggled via environment variables without breaking offline fallback.

2. **Multilingual Speech & Audio Intelligence**
   - **Speech-to-Text (STT):** Browser Web Speech Recognition API supporting `hi-IN` (Hindi), `en-IN` (Indian English), and romanized Hinglish phonetics.
   - **Text-to-Speech (TTS):** Browser SpeechSynthesis API with dialect-matched voices, markdown and disclaimer sanitization, auto-mute toggles, and replay controls.
   - **Real-Time Audio Visualizer:** Web Audio API (`AudioContext` + `AnalyserNode`) extracting live Root Mean Square (RMS) microphone energy.
   - **Dynamic Canvas Waveform:** Custom reactive multi-harmonic canvas rendering real-time speech energy and state transitions (`idle`, `listening`, `processing`).

3. **Deterministic Clinical Conversation Engine**
   - **Multilingual Symptom Normalizer:** Maps Romanized Hinglish (*"mujhe bukhar hai"*, *"pet me dard"*), Devanagari Hindi (*"मुझे खांसी है"*), and English expressions to standard clinical symptom concepts.
   - **Acute Safety & Red Flag Interceptor:** Dedicated screening for cardiac, stroke, respiratory distress, and severe trauma red flags.
   - **Context & Negation Hardening:** Distinguishes negations (*"no chest pain"*), past history (*"had fever last month"*), third-party mentions (*"my mother has diabetes"*), and resolved symptoms.
   - **Clinical Pathways:** 4 dedicated interactive triage pathways (Fever, Cough, Headache, Abdominal Pain). Enforces a strict maximum of 4 targeted follow-up questions and automatically skips questions already answered in initial user input.

4. **Structured Non-Prescriptive Clinical Assessments**
   - Separates verified patient-reported facts from clinical interpretations.
   - States timeline, missing clinical information, and potential non-diagnostic explanations without inventing false probability percentages or guessing single-symptom diseases.
   - Strictly prohibits prescription medicine or dosage recommendations; provides lifestyle and professional care navigation instead.

5. **Doctor & Hospital Discovery Network**
   - **Doctor Directory:** Filterable by city (Bengaluru, Delhi NCR, Mumbai, Jaipur, Chennai), medical specialty, and teleconsultation availability.
   - **Hospital & Emergency Network:** Directory of accredited tertiary hospitals, 24x7 trauma centers, ICU availability, direct helpline/ambulance dialers, and clinical departments.
   - **Appointment & Triage Enquiry:** Interactive modal for teleconsult or in-person appointment requests with instant confirmation tracking IDs.

6. **Consultation History & Resumption**
   - Full persistence in SQLite with SQLAlchemy ORM.
   - Review past consultations, dialogue transcripts, and clinical summaries.
   - One-click resumption of any previous consultation directly into the interactive chat view.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, TypeScript (Strict), Vite, Tailwind CSS, Lucide React |
| **Voice & Audio** | Web Speech API (`webkitSpeechRecognition`), SpeechSynthesis, Web Audio API (`AnalyserNode`), HTML5 Canvas |
| **Backend** | Python 3.12 / 3.13, FastAPI, SQLAlchemy ORM, Pydantic v2 |
| **Database** | SQLite3 with persistent session models and transcripts |
| **Containerization** | Docker & Docker Compose |
| **Design System** | Tailored Warm Ivory (`#FDFBF7`), Surface (`#F7F4EE`), Deep Forest Green (`#1E3A2F`), Muted Sage (`#6B8E7C`) palette |

---

## 🚀 Quickstart (Local Development)

### 1. Prerequisites
- **Node.js**: v18+ (Tested on v22.x)
- **Python**: v3.11+ (Tested on v3.13.9) with `uv` or `pip`

### 2. Backend Setup
```bash
# Navigate to the backend directory
cd backend

# Create virtual environment and install dependencies
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Start backend server on port 8001
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```
Verify backend status:
```bash
curl http://127.0.0.1:8001/api/v1/health
```

### 3. Frontend Setup
```bash
# In a new terminal window:
cd frontend

# Install dependencies
npm install

# Start Vite development server (proxies /api to port 8001)
npm run dev
```
Open **[http://localhost:5173](http://localhost:5173)** in Google Chrome or Microsoft Edge for optimal Web Speech API voice support.

---

## 🐳 Docker Deployment

To build and run both frontend and backend in isolated containers:

```bash
docker compose up --build
```

- **Frontend Application:** [http://localhost:5173](http://localhost:5173)
- **FastAPI Interactive Docs:** [http://localhost:8001/docs](http://localhost:8001/docs)
- **Healthcheck Endpoint:** [http://localhost:8001/api/v1/health](http://localhost:8001/api/v1/health)

---




## ⚖️ Clinical Safety & Legal Disclaimer

CuraGennie is a health education, symptom understanding, and clinical navigation prototype. It is **not** a licensed medical practitioner, medical device, or diagnostic system. It does not prescribe medications, calculate drug dosages, or provide definitive diagnostic determinations. 

If you or someone nearby experiences symptoms such as severe chest pain, shortness of breath, sudden weakness or numbness, slurred speech, or unexplained loss of consciousness, immediately call **112** or **108** in India, or proceed to the nearest hospital emergency room.
