# CURAGENNIE — HACKATHON SUBMISSION CHECKLIST
## Deadline: 30 November 2026, 11:59 PM IST

Use this checklist to verify that all submission rules are 100% satisfied before submitting the form.

---

### Item 1: Code on GitHub
- [x] **Public GitHub Repository:** Ensure repository visibility is set to **Public** so judges can open and clone it.
- [x] **Docker Setup File (`docker-compose.yml`):**
  - Present in repository root.
  - Boots backend (port 8001) and frontend (port 5173) in one command: `docker compose up --build`.
  - Includes healthcheck for zero-downtime startup.
- [x] **Zero Secret Keys Guarantee:**
  - Tested: boots and operates completely without any OpenAI, Gemini, or external API keys.
  - Fully deterministic local clinical conversation engine with SQLite database.
- [x] **Code Volume & Originality:**
  - Over **2,400+ lines** of original TypeScript and Python code written during the hackathon.
  - Complete custom components: Voice STT/TTS hooks, Audio RMS analyzer, Canvas waveform, multilingual normalizer, 4 clinical pathways, emergency safety interceptor, doctor/hospital discovery, and printable summaries.
- [x] **Automated Test Suite:**
  - 46 unit and integration tests passing (`PYTHONPATH=. pytest tests/ -v`).
  - Zero TypeScript compile errors (`npm run build`).

---

### Item 2: Demo Video on YouTube
- [ ] **Video Length:** 3 minutes or less (strict requirement).
- [ ] **Visibility:** Public or Unlisted on YouTube.
- [ ] **Content Demonstrated:**
  - Natural Hinglish voice consultation with live audio visualizer.
  - Clinical follow-up questions and pre-answered question skipping.
  - Structured non-diagnostic clinical summary with printable handover sheet.
  - Critical emergency escalation (112/108) on acute chest pain.
  - Doctor and hospital network discovery with appointment enquiry.
- [ ] **Reference Script:** Use [`docs/DEMO_VIDEO_SCRIPT.md`](./DEMO_VIDEO_SCRIPT.md).

---

### Item 3: Pitch Deck (PDF)
- [ ] **Format:** PDF document uploaded to submission form or Google Drive link.
- [ ] **Word-Focused:** Content is clear, structured text (judges read the words, not decorative graphics).
- [ ] **Mandatory Questions Covered:**
  - [x] Problem and solution: Who has the problem and how CuraGennie solves it.
  - [x] Who it is for & market size: Tier 1/2/3 Indian population, non-English-first households, TAM/SAM/SOM.
  - [x] Dependencies & Cost Resiliency: Web Speech API (zero cost), local Python state machine (zero cost), and fallback behavior if voice or AI services fail or become costly.
  - [x] Launch plan: Community triage pilots, WhatsApp web integration, and clinic partnerships.
- [ ] **Reference Content:** Use [`docs/PITCH_DECK.md`](./PITCH_DECK.md).

---

### Item 4: Live Link (Optional Bonus)
- Optional bonus point. If deployed (e.g. Render, Railway, or AWS/DigitalOcean), paste the URL in the submission form.
- The app functions 100% locally with Docker regardless of live deployment.
