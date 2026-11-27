# CURAGENNIE — HACKATHON PITCH DECK
## Scaler × Wispr Flow Hackathon Submission
*(Copy/paste or export this text directly to your pitch deck slides or PDF generator. Designed specifically to satisfy the text-focused judging requirements).*

---

### SLIDE 1: Title & Vision
- **Product Name:** CuraGennie
- **Tagline:** "Your health deserves to be heard."
- **Category:** HealthTech / MedTech / Conversational AI
- **One-Line Elevator Pitch:** A voice-first, multilingual healthcare assistant that helps Indian families describe their symptoms naturally in Hindi, Hinglish, or English, screens for acute emergency red flags, and navigates them toward appropriate doctor and hospital care.
- **Team:** CuraGennie Team (Shiv Rajawat & Team)

---

### SLIDE 2: The Problem — The Pre-Doctor Dilemma in India
- **The Core Issue:** Over 70% of healthcare hesitation in India happens **before** a patient ever sees a doctor or visits a clinic.
- **Specific Pain Points:**
  1. **Language Barrier:** Most digital health apps are English-only and form-heavy; Indian patients think and communicate naturally in Hinglish (*"2 din se bukhar aur badan dard hai"*) or Hindi.
  2. **Medical Jargon & Anxiety:** Patients struggle to articulate clinical symptoms, leading to delayed visits or dangerous self-medication (OTC antibiotics/NSAIDs).
  3. **Triage Confusion:** Patients don't know whether a symptom is benign, requires an OPD general physician, needs a specialist, or is an acute emergency.
  4. **Digital Exclusion:** Elderly, rural, and non-tech-savvy users are alienated by complex, dropdown-heavy portals.

---

### SLIDE 3: The Solution — Voice-First Conversational Navigation
- **Natural Voice Interaction:** Users tap a microphone and speak conversationally in Hindi, Hinglish, or English.
- **Context-Aware Clinical State Machine:** CuraGennie asks a strict maximum of 4 targeted follow-up questions, tracks conversation memory, and automatically skips questions the user has already answered.
- **Safety-First Emergency Interceptor:** Screens for cardiac, stroke, and respiratory red flags. Immediately halts routine questioning and triggers India’s national emergency protocol (112 / 108).
- **Structured Non-Prescriptive Assessments:** Generates clear clinical summaries separating patient facts from interpretations, without inventing disease probabilities or prescribing drugs.
- **Doctor & Hospital Discovery:** Seamlessly connects patients to verified specialists and tertiary 24x7 emergency/ICU facilities with instant appointment tracking.

---

### SLIDE 4: Who It Is For & Market Size (Target Audience)
- **Primary Audience:**
  - **Indian Households (Tier 1, 2, and 3):** Over 600M+ smartphone users in India who are comfortable speaking in their regional dialect or Hinglish rather than typing in formal English.
  - **Elderly & Digitally Hesitant Users:** Benefiting from voice-guided dialogue rather than complex form-filling.
  - **Caregivers & Parents:** Quickly triaging children’s or elderly parents’ complaints to determine if emergency attention is needed.
- **Market Opportunity:**
  - **Total Addressable Market (TAM):** Indian Digital Health Market projected to reach \$25B+ by 2027.
  - **Serviceable Available Market (SAM):** 250M+ non-English-dominant digital healthcare searchers in India.
  - **Serviceable Obtainable Market (SOM):** Initial launch targeting 100,000 active outpatient triage navigation sessions across urban and semi-urban clusters.

---

### SLIDE 5: Product Architecture & The Zero-Key Advantage
- **Frontend Layer:** React 18, TypeScript, Tailwind CSS, Web Speech API (STT & TTS), Web Audio API (real-time RMS energy), HTML5 Canvas dynamic waveform.
- **Intelligence Layer:** FastAPI + Python clinical state machine, multilingual normalization dictionary, negation and temporal safety engine.
- **Database & Persistence:** SQLite3 + SQLAlchemy ORM for instant session resumption and clinical transcript audits.
- **The Zero-Key Guarantee:** CuraGennie is engineered to run 100% locally and deterministically. Evaluators can boot the entire system with `docker compose up` without providing external OpenAI or Gemini API keys.

---

### SLIDE 6: Dependencies, Cost Resiliency & Fallback Strategy
*(Addressing Hackathon Requirement: "What it depends on... and what happens if they get costly or stop working")*
- **1. Voice Recognition & Speech Synthesis:**
  - *Dependency:* Browser-native Web Speech API (`webkitSpeechRecognition` & `speechSynthesis`).
  - *Cost:* **₹0 / Zero per-minute server cost.** Runs client-side on the user's browser engine.
  - *Failure Contingency:* If an unsupported browser (e.g. Safari) or blocked microphone is detected, CuraGennie automatically falls back to universal text input with zero disruption to the consultation.
- **2. Core Clinical Conversation Intelligence:**
  - *Dependency:* Deterministic Python conversation engine with multilingual synonym maps.
  - *Cost:* **₹0 / Zero external token fees.** Runs locally with predictable sub-50ms latency.
  - *Failure Contingency:* 100% immune to external LLM downtime, API rate limits, or price surges.
- **3. Optional External LLM Provider (Future Enhancement):**
  - *Contingency:* If an external LLM is toggled on and encounters downtime or exceeds budget limits, CuraGennie instantly reverts to the built-in deterministic safety engine without dropping the user's session.

---

### SLIDE 7: Safety, Ethics & Clinical Boundaries
- **Non-Diagnostic Policy:** CuraGennie explicitly clarifies that it does not provide confirmed medical diagnoses.
- **Zero Prescriptions / Dosages:** Never suggests prescription pharmaceuticals or dosage calculations. Recommends safe hydration/rest and directs to licensed clinicians.
- **Emergency Priority:** Routine questions are aborted upon detecting critical red flags, flashing prominent 112 / 108 emergency dialers.
- **Privacy & Data Minimization:** No raw microphone audio is ever stored on servers; all audio processing is transient.

---

### SLIDE 8: Go-To-Market & Launch Plan
- **Phase 1 (Month 1–3): Community & WhatsApp Entry:**
  - Launch web prototype and lightweight WhatsApp voice bot integration for seamless access.
  - Partner with regional healthcare clinics in Bengaluru and Jaipur for pilot triage kiosk deployments.
- **Phase 2 (Month 4–6): Provider Partnerships:**
  - Partner with diagnostic chains and teleconsultation platforms to monetize appointment and lab test referrals.
  - Provide structured "Print / Handover Summaries" to partner clinics to save doctor intake time by 40%.
- **Phase 3 (Month 7+): B2B Enterprise Integration:**
  - White-label voice intake SDK for hospital apps, health insurance providers, and corporate employee wellness desks.

---

### SLIDE 9: Competitive Differentiation
| Dimension | Traditional Chatbots | Static Symptom Checkers | **CuraGennie** |
| :--- | :--- | :--- | :--- |
| **Input Modality** | Typing only | Form dropdowns & radio buttons | **Voice-First (Hindi/Hinglish/English)** |
| **Language** | English-centric | English-centric | **True Multilingual & Phonetic Hinglish** |
| **Safety Interceptor**| Post-conversation text disclaimer | Static list | **Real-time Emergency Escalation (112/108)** |
| **Operating Cost** | High token bills per conversation | Static server | **Zero-Key Deterministic Engine (Zero cost)** |
| **Navigation** | General advice only | Generic links | **Doctor & Hospital Network with Enquiries** |

---

### SLIDE 10: Conclusion & Hackathon Submission Summary
- **Functional Prototype Ready:** Fully runnable via `docker compose up` on port 5173/8001.
- **Zero Secrets Required:** Ready for one-command judging evaluation.
- **Scalable Impact:** Solving the crucial "pre-doctor" hesitation for millions of non-English-first Indian citizens.
- **GitHub Repository:** Public on GitHub.
- **Next Step:** Advancing toward the Grand Finale with real clinic integration and expanded regional language models.
