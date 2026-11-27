# CURAGENNIE — 3-MINUTE DEMO VIDEO SCRIPT
## Scaler × Wispr Flow Hackathon Video Walkthrough (Under 180 Seconds)

> **Video Target Duration:** 2 minutes 50 seconds (well under the 3:00 minute hard limit).  
> **Format:** Screen recording of browser with microphone audio.

---

### [0:00 – 0:25] ACT 1: Introduction & The Problem in India
- **Visual:** Show CuraGennie Dashboard at `http://localhost:5173`. Point out the clean healthcare design system, "Zero-Key Engine" status indicator, and brand identity.
- **Spoken Audio:**
  > *"Hello judges! Over 70% of healthcare hesitation in India happens before a patient ever reaches a doctor. Millions of Indian citizens think in Hindi or Hinglish, struggle with complex medical forms, and don't know whether their symptoms need a routine doctor visit or an emergency room.  
  > This is **CuraGennie** — a serious, voice-first personal healthcare assistant designed specifically for Indian families. It operates 100% out-of-the-box with zero required external API keys."*

---

### [0:25 – 1:15] ACT 2: Voice-First Hinglish Triage & Live Waveform
- **Visual:** 
  1. Click on **New Consultation**.
  2. Select **Hinglish** language toggle.
  3. Point to the **Web Speech Ready** indicator in the header.
  4. Tap the **Microphone** icon. Speak or click prompt:
     *"Mujhe do din se tez bukhar hai aur badan me dard ho raha hai"*
  5. Show the live multi-harmonic canvas waveform reacting dynamically to voice volume.
  6. Show the interim speech transcript populating live.
  7. Hit Send.
- **Spoken Audio:**
  > *"Let's test a natural consultation in Hinglish. I simply tap the mic and say: 'Mujhe do din se tez bukhar hai aur badan me dard ho raha hai'. Notice the live audio-reactive canvas waveform measuring microphone RMS energy in real time.  
  > The engine normalizes our colloquial Hinglish into clinical symptoms, activates the dedicated Fever Pathway, and asks its first targeted follow-up question regarding temperature."*

---

### [1:15 – 1:55] ACT 3: Smart Question Skipping & Structured Clinical Summary
- **Visual:**
  1. Assistant asks: *"Have you measured your body temperature with a thermometer?"*
  2. Reply by voice or typing: *"Yes, temperature 102 hai aur koi skin rash nahi hai"*
  3. Notice how CuraGennie records the temperature AND records the negative rash, automatically skipping the rash question.
  4. Complete the remaining questions (under 4 questions).
  5. The **Structured Clinical Assessment** card renders.
  6. Click the new **"Print / Export Summary"** button to showcase the formal clinical handover sheet.
- **Spoken Audio:**
  > *"Watch how smart the clinical engine is: when I answer 'Temperature 102 hai aur koi rash nahi hai', it registers the temperature AND skips asking about rash later because I already answered it. Enforcing a strict 4-question limit prevents patient fatigue.  
  > When complete, it generates a structured, non-diagnostic clinical assessment separating verified patient facts from clinical interpretations. And with one click, patients can print or save a clean clinical handover sheet to take directly to their doctor!"*

---

### [1:55 – 2:25] ACT 4: Critical Emergency Escalation (The Red Flag Interceptor)
- **Visual:**
  1. Click **Start Fresh Consultation**.
  2. Speak or enter acute cardiac symptoms:
     *"Severe crushing chest pain radiating to my left arm and heavy sweating"*
  3. Show the instant emergency escalation:
     - Questioning halts immediately.
     - Pulsing red emergency alert flashes.
     - Direct one-click dial buttons appear for **112 (National Emergency)** and **108 (Ambulance)**.
- **Spoken Audio:**
  > *"Now watch our safety architecture in action. What if a user mentions an acute warning sign? I'll say: 'Severe crushing chest pain radiating to left arm and cold sweating'.  
  > Instantly, routine questioning is stopped. CuraGennie detects a critical cardiac red flag, flashes an emergency alert, and provides direct one-tap dialing for National Emergency 112 and Ambulance 108. It never provides false reassurance or diagnostic guesswork when lives are on the line."*

---

### [2:25 – 2:45] ACT 5: Doctor & Hospital Discovery Network
- **Visual:**
  1. Click **Hospital Network** in sidebar.
  2. Filter by city (*Bengaluru*) and toggle **24x7 Emergency Only**.
  3. Click **Enquire / Book** on Apollo Hospitals.
  4. Type patient name, phone, and submit.
  5. Show the instant confirmation notice with reference tracking ID: `enq-xxxx`.
- **Spoken Audio:**
  > *"Next, CuraGennie closes the loop by navigating patients to care. Our Hospital Network allows filtering accredited tertiary hospitals by city, clinical departments, and 24x7 ICU availability. Patients can book teleconsultations with verified specialists or submit hospital admission enquiries with instant tracking."*

---

### [2:45 – 3:00] ACT 6: Conclusion & Submission Wrap-Up
- **Visual:** Show the repository on GitHub with `docker-compose.yml`, 46 passing tests, and clean architecture.
- **Spoken Audio:**
  > *"CuraGennie runs entirely via `docker compose up` with zero external API keys needed, backed by 46 automated clinical safety tests. Thank you Scaler and Wispr Flow for this opportunity — because every citizen's health deserves to be heard!"*

---

### Recording Checklist
- [ ] Browser set to Google Chrome or Microsoft Edge (at 100% or 110% zoom for crisp readability).
- [ ] Microphone input tested and clear.
- [ ] Both frontend (`localhost:5173`) and backend (`localhost:8001`) running smoothly.
- [ ] Timer running to keep total recording under 3 minutes.
- [ ] Video uploaded to YouTube as **Public** or **Unlisted**.
