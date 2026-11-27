"""Comprehensive test suite for the CuraGennie Healthcare Conversation Engine and Safety Architecture.
Validates:
1. Multilingual Symptom Normalization (English, Hindi, Hinglish)
2. Safety Engine & Red-flag Emergency Detection
3. Negation Resolution
4. Historical/Past Symptom Filtering
5. Ambiguity Handling
6. 4 Clinical Pathways (Fever, Cough, Headache, Abdominal Pain)
7. Max 4 Questions Enforcement
8. Context Memory & Skipping Pre-answered Questions
9. Assessment Generation & Cautious Non-Diagnostic Framing
10. Database Persistence & Session Resumption
11. REST API Endpoints & Zero-Key Operation
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import init_db, SessionLocal
from app.models.session import ConsultationSession
from app.services.symptom_normalizer import symptom_normalizer
from app.services.safety_engine import safety_engine
from app.services.questioning_engine import questioning_engine
from app.services.assessment_engine import assessment_engine
from app.services.consultation_engine import consultation_engine
from app.schemas.conversation import ConversationState
from app.medical_data.symptom_dictionary import (
    FEVER,
    BODY_PAIN,
    HEADACHE,
    COUGH,
    NAUSEA_VOMITING,
    ABDOMINAL_PAIN,
)

init_db()
client = TestClient(app)


# ============================================================================
# 1. SYMPTOM NORMALIZATION TESTS (English, Hindi, Hinglish)
# ============================================================================

def test_normalization_english_symptoms():
    res1 = symptom_normalizer.normalize("I have had a high fever and body ache since 2 days")
    assert FEVER in res1.detected_symptoms
    assert BODY_PAIN in res1.detected_symptoms
    assert res1.timeline is not None

    res2 = symptom_normalizer.normalize("Persistent dry cough with throat pain")
    assert COUGH in res2.detected_symptoms


def test_normalization_hinglish_symptoms():
    res1 = symptom_normalizer.normalize("mujhe 2 din se bukhar hai aur body mein dard hai")
    assert FEVER in res1.detected_symptoms
    assert BODY_PAIN in res1.detected_symptoms
    assert "2 din" in res1.timeline

    res2 = symptom_normalizer.normalize("kal raat se sar mein dard ho raha hai aur chakkar aa rahe hain")
    assert HEADACHE in res2.detected_symptoms

    res3 = symptom_normalizer.normalize("khansi ho rahi hai aur gale me kharash hai")
    assert COUGH in res3.detected_symptoms

    res4 = symptom_normalizer.normalize("pet dard ho raha hai aur ulti aa rahi hai")
    assert ABDOMINAL_PAIN in res4.detected_symptoms
    assert NAUSEA_VOMITING in res4.detected_symptoms


def test_normalization_hindi_devanagari():
    res1 = symptom_normalizer.normalize("मुझे दो दिन से तेज बुखार और बदन दर्द है")
    assert FEVER in res1.detected_symptoms
    assert BODY_PAIN in res1.detected_symptoms

    res2 = symptom_normalizer.normalize("पेट में बहुत तेज दर्द और उल्टी हो रही है")
    assert ABDOMINAL_PAIN in res2.detected_symptoms
    assert NAUSEA_VOMITING in res2.detected_symptoms


# ============================================================================
# 2. SAFETY ENGINE & EMERGENCY ESCALATION TESTS
# ============================================================================

def test_safety_positive_cardiac_emergency():
    # Severe chest pain with radiation
    eval_en = safety_engine.evaluate("I have severe chest pain radiating to my left arm and sweating")
    assert eval_en.is_emergency is True
    assert len(eval_en.triggered_flags) > 0
    assert "112" in eval_en.emergency_message

    eval_hi = safety_engine.evaluate("chhati me tez dard ho raha hai aur baye haath me dard ja raha hai")
    assert eval_hi.is_emergency is True
    assert "112" in eval_hi.emergency_message


def test_safety_positive_respiratory_distress():
    eval_res = safety_engine.evaluate("I cannot breathe, gasping for air and lips turning blue")
    assert eval_res.is_emergency is True


def test_safety_positive_stroke_signs():
    eval_res = safety_engine.evaluate("My mother's facial drooping suddenly and she has slurred speech")
    assert eval_res.is_emergency is True


def test_safety_positive_thunderclap_headache():
    eval_res = safety_engine.evaluate("This is the worst headache of my life, sudden explosive pain")
    assert eval_res.is_emergency is True


# ============================================================================
# 3. NEGATION HANDLING TESTS (Rule A: Negation must not trigger emergency)
# ============================================================================

def test_safety_negation_english():
    eval_res1 = safety_engine.evaluate("I have a mild headache, but I do not have chest pain")
    assert eval_res1.is_emergency is False

    eval_res2 = safety_engine.evaluate("I am free of chest pain and have no shortness of breath")
    assert eval_res2.is_emergency is False


def test_safety_negation_hinglish_and_hindi():
    eval_res1 = safety_engine.evaluate("mujhe bukhar hai lekin chhati me dard nahi hai")
    assert eval_res1.is_emergency is False

    eval_res2 = safety_engine.evaluate("sar dard hai par saans lene me koi dikkat nahi hai")
    assert eval_res2.is_emergency is False

    eval_res3 = safety_engine.evaluate("बुखार है लेकिन सीने में दर्द नहीं है")
    assert eval_res3.is_emergency is False


# ============================================================================
# 4. HISTORICAL CONTEXT TESTS (Rule B: Past events must not trigger emergency)
# ============================================================================

def test_safety_historical_events():
    eval_en = safety_engine.evaluate("I had severe chest pain last month, but today I only have a cold")
    assert eval_en.is_emergency is False
    assert eval_en.is_historical is True

    eval_hi = safety_engine.evaluate("pichle saal behosh hua tha, aaj sirf halka bukhar hai")
    assert eval_hi.is_emergency is False
    assert eval_hi.is_historical is True


# ============================================================================
# 5. AMBIGUITY HANDLING TESTS (Rule C: Ambiguous mentions trigger clarification)
# ============================================================================

def test_safety_ambiguity_handling():
    eval_res = safety_engine.evaluate("maybe chest pain or gas, not sure if severe pressure")
    assert eval_res.is_emergency is False
    assert eval_res.is_ambiguous is True
    assert eval_res.clarification_prompt is not None


# ============================================================================
# 6. FOUR PATHWAYS & FOLLOW-UP QUESTION TESTS
# ============================================================================

def test_fever_pathway_flow():
    db = SessionLocal()
    try:
        # Step 1: Start
        res1 = consultation_engine.start_session(db, language="hinglish")
        sid = res1.session_id

        # Step 2: Intake - Report fever
        res2 = consultation_engine.process_user_message(db, sid, "Mujhe 2 din se bukhar hai")
        assert res2.state == ConversationState.FOLLOW_UP
        assert res2.next_question is not None
        assert res2.next_question.question_index == 1

        # Step 3: Answer temperature
        res3 = consultation_engine.process_user_message(db, sid, "Haan naapa tha, 101.5 f tha")
        assert res3.state == ConversationState.FOLLOW_UP
        assert res3.next_question.question_index == 2

        # Step 4: Answer associated symptoms
        res4 = consultation_engine.process_user_message(db, sid, "Thand lag rahi hai aur thoda badan dard hai")
        assert res4.state == ConversationState.FOLLOW_UP

        # Step 5: Answer hydration
        res5 = consultation_engine.process_user_message(db, sid, "Paani pee pa raha hoon, ulti nahi hai")
        assert res5.state in [ConversationState.FOLLOW_UP, ConversationState.ASSESSMENT]
    finally:
        db.close()


def test_cough_pathway_flow():
    db = SessionLocal()
    try:
        res1 = consultation_engine.start_session(db, language="en", chief_complaint="I have a bad cough")
        assert res1.state == ConversationState.FOLLOW_UP
        assert "dry" in res1.assistant_message.lower() or "cough" in res1.assistant_message.lower()
    finally:
        db.close()


def test_max_four_questions_enforcement():
    db = SessionLocal()
    try:
        res = consultation_engine.start_session(db, language="hinglish", chief_complaint="Sar me dard hai")
        sid = res.session_id

        # Simulate 4 sequential answers
        turns = 0
        while res.state == ConversationState.FOLLOW_UP and turns < 6:
            res = consultation_engine.process_user_message(db, sid, f"Answer turn {turns+1}")
            turns += 1

        # Must conclude in ASSESSMENT and ask no more than 4 follow-up questions
        session = db.query(ConsultationSession).filter(ConsultationSession.id == sid).first()
        assert session.follow_up_count <= 4
        assert res.state == ConversationState.ASSESSMENT
        assert res.assessment is not None
    finally:
        db.close()


def test_skipping_preanswered_questions():
    # If the user already states fever duration and temperature in the intake,
    # questioning engine should not ask them again
    collected = {
        "duration": "3 days",
        "temperature_reading": "102 F",
    }
    next_q = questioning_engine.get_next_question(
        pathway="fever",
        asked_question_ids=[],
        collected_data=collected,
        language="en",
    )
    # The first question (duration) and second (temp) should be skipped
    assert next_q is not None
    assert next_q.id == "fever_associated"


# ============================================================================
# 7. ASSESSMENT GENERATION TESTS (Cautious Non-Diagnostic Framing)
# ============================================================================

def test_assessment_non_prescriptive_content():
    assessment = assessment_engine.generate_assessment(
        chief_complaint="Bukhar aur khansi",
        pathway="fever",
        detected_symptoms=["fever", "cough"],
        collected_data={"timeline": "2 din se", "temperature_reading": "101 F"},
        follow_up_answers={"fever_associated": "badan dard hai"},
        red_flags_identified=[],
        is_escalated=False,
    )

    assert assessment.professional_consultation_recommended is True
    assert len(assessment.potential_explanations) > 0
    # Must contain disclaimer
    assert "not a confirmed medical diagnosis" in assessment.disclaimer.lower()
    assert len(assessment.suggested_next_steps) > 0


# ============================================================================
# 8. PERSISTENCE & RESUMPTION TESTS
# ============================================================================

def test_session_persistence_and_resumption():
    db = SessionLocal()
    try:
        # Create session
        res1 = consultation_engine.start_session(db, language="hinglish", chief_complaint="Pet me dard hai")
        sid = res1.session_id

        # Add message
        consultation_engine.process_user_message(db, sid, "Kal raat se naabhi ke paas marod ho rahi hai")

        # Resume session detail
        detail = consultation_engine.get_session_detail(db, sid)
        assert detail.session_id == sid
        assert detail.chief_complaint == "Pet me dard hai"
        assert len(detail.messages) >= 2
    finally:
        db.close()


# ============================================================================
# 9. API REST ENDPOINT TESTS
# ============================================================================

def test_api_start_consultation():
    response = client.post("/api/v1/consultations/start", json={"language": "hinglish"})
    assert response.status_code == 201
    data = response.json()
    assert "session_id" in data
    assert data["state"] == "INTAKE"


def test_api_message_and_emergency_escalation():
    # 1. Start session
    start_res = client.post("/api/v1/consultations/start", json={"language": "en"})
    sid = start_res.json()["session_id"]

    # 2. Trigger acute emergency via API
    msg_res = client.post(
        f"/api/v1/consultations/{sid}/message",
        json={"content": "I am having severe crushing chest pain radiating to my arm and cold sweats"},
    )
    assert msg_res.status_code == 200
    data = msg_res.json()
    assert data["state"] == "ESCALATED"
    assert data["safety_status"]["is_emergency"] is True
    assert "112" in data["assistant_message"]


def test_api_zero_external_key_operation():
    # Health check confirms zero-key mode
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["details"]["zero_key_mode"] is True
    assert data["mode"] == "deterministic_local"
