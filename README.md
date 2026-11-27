# CuraGennie — Voice-First AI Healthcare Assistant

> **"Your health deserves to be heard."**  
> Scaler × Wispr Flow Hackathon Project

CuraGennie is a serious, voice-first personal healthcare assistant designed for Indian families. It allows users to describe health concerns naturally in **Hindi**, **Hinglish**, or **English**, detects critical emergency red flags, asks targeted follow-up questions, and recommends appropriate care pathways.

---

## 🌟 Key Architecture Highlights

- **Zero-Key Out-of-the-Box Guarantee:** Runs 100% locally with deterministic medical triage rules. No external OpenAI/Gemini API key is required to boot, test, or evaluate the system.
- **Voice-First Navigation:** Built with the browser Web Speech API (`SpeechRecognition` & `SpeechSynthesis`) and audio visualization.
- **Emergency Interceptor:** Deterministic red-flag dictionary for immediate acute triage (e.g. chest pressure, severe breathlessness, stroke signs) directing patients to Indian national emergency services (112 / 108).
- **Multilingual Support:** Handles colloquial Hinglish, Hindi, and Indian English with medical synonym normalization.
- **Clinical Doctor Discovery:** Directory of verified Indian specialties and clinicians across cities (Bengaluru, Delhi NCR, Mumbai, Jaipur, Chennai).

---

## 🛠️ Tech Stack

- **Frontend:** React 18, TypeScript (Strict), Vite, Tailwind CSS, Lucide React.
- **Backend:** Python 3.12/3.13, FastAPI, SQLAlchemy ORM, Pydantic v2.
- **Database:** SQLite3 with persistent session history.
- **Containerization:** Docker & Docker Compose.

---

## 🚀 Quickstart (Local Development)

### 1. Prerequisites
- **Node.js**: v18+ (Tested on v22.23.1)
- **Python**: v3.11+ (Tested on v3.13.9) with `uv` or `pip`

### 2. Backend Setup
```bash
# In the repository root:
cd backend

# Create virtual environment and install dependencies using uv:
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Start backend server on port 8001:
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```
Verify backend is online:
```bash
curl http://127.0.0.1:8001/api/v1/health
```

### 3. Frontend Setup
```bash
# In a new terminal window:
cd frontend

# Install dependencies:
npm install

# Start Vite development server:
npm run dev
```
Open **[http://localhost:5173](http://localhost:5173)** in your browser.

---

## 🐳 Docker Deployment

To build and run both frontend and backend in isolated containers:

```bash
docker compose up --build
```

- **Frontend:** [http://localhost:5173](http://localhost:5173)
- **Backend API Docs:** [http://localhost:8001/docs](http://localhost:8001/docs)
- **Healthcheck:** [http://localhost:8001/api/v1/health](http://localhost:8001/api/v1/health)

*(Note: If Docker is not yet installed on macOS, install Docker Desktop or OrbStack via `brew install --cask docker`)*

---

## 🧪 Testing

### Backend Automated Unit Tests
```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

### Frontend Typecheck & Production Build
```bash
cd frontend
npm run build
```

---

## 📋 Project Status

| Phase | Description | Status |
| :--- | :--- | :--- |
| **Phase 00** | Workspace Audit & Engineering Plan | ✅ Complete |
| **Phase 01** | Project Scaffolding & Design Foundation | ✅ Complete |
| **Phase 02** | Deterministic Medical Engine & Triage State Machine | ⏳ Next |
| **Phase 03** | Web Speech Voice Audio Engine & Waveform | ⏳ Upcoming |
| **Phase 04** | Clinical Summaries, Doctor Booking & Optional LLM | ⏳ Upcoming |
| **Phase 05** | Production Hardening, Docker & End-to-End QA | ⏳ Upcoming |

---

## ⚖️ Clinical Disclaimer

CuraGennie is a health guidance, navigation, and education tool. It is **not** an autonomous diagnostic or prescription system. In case of acute medical emergencies, immediately contact local emergency healthcare providers or call **112** / **108** in India.
