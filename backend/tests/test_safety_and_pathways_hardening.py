"""Comprehensive safety context handling and 4-pathway hardening test suite for CuraGennie.
Covers:
1. Complete 4-Pathway testing (Fever, Cough, Headache, Abdominal Pain)
   - Normal progression
   - Skipping pre-answered questions
   - Max 4 questions enforcement
   - Assessment generation
   - Mid-consultation emergency interruption
2. Safety Context Handling:
   - English & Hindi negation
   - Past vs current symptoms
   - Uncertainty & ambiguous descriptions
   - Symptoms belonging to another person
   - Multiple people mentioned in one turn
   - Resolved vs ongoing symptoms
3. Medical Assessment Engine Audit:
   - Undifferentiated single nonspecific symptoms
   - Zero invented probability percentages
   - Explicit missing clinical data
   - Fact vs interpretation separation
   - No prescription medicines / no false reassurance
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
    COUGH,
    HEADACHE,
    ABDOMINAL_PAIN,
)

init_db()
client = TestClient(app)


# ============================================================================
# 1. COMPLETE 4-PATHWAY TESTS
# ============================================================================

class TestFourPathways:
    def test_fever_pathway_complete_lifecycle(self):
        db = SessionLocal()
        try:
            # Step 1: Start
            res = consultation_engine.start_session(db, language="hinglish", chief_complaint="Mujhe bukhar hai")
            sid = res.session_id
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "fever_duration"

            # Step 2: Duration
            res = consultation_engine.process_user_message(db, sid, "3 din se bukhar chal raha hai")
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "fever_temperature"

            # Step 3: Temperature
            res = consultation_engine.process_user_message(db, sid, "102 degree tha thermometer par")
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "fever_associated"

            # Step 4: Associated
            res = consultation_engine.process_user_message(db, sid, "Thand lag rahi hai aur sar dard bhi hai")
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "fever_hydration_warning"

            # Step 5: Hydration -> Assessment
            res = consultation_engine.process_user_message(db, sid, "Fluids pee raha hoon koi ulti nahi hai")
            assert res.state == ConversationState.ASSESSMENT
            assert res.assessment is not None
            assert res.assessment.professional_consultation_recommended is True
        finally:
            db.close()

    def test_cough_pathway_complete_lifecycle(self):
        db = SessionLocal()
        try:
            res = consultation_engine.start_session(db, language="en", chief_complaint="I have a persistent cough")
            sid = res.session_id
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "cough_duration"

            # Provide duration
            res = consultation_engine.process_user_message(db, sid, "It started 5 days ago after a slight cold")
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "cough_type"

            # Provide cough type
            res = consultation_engine.process_user_message(db, sid, "It is a dry cough, no phlegm")
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "cough_associated"

            # Provide associated
            res = consultation_engine.process_user_message(db, sid, "No fever, just throat irritation")
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "cough_breathing_warning"

            # Answer breathing warning -> Assessment
            res = consultation_engine.process_user_message(db, sid, "No shortness of breath")
            assert res.state == ConversationState.ASSESSMENT
            assert res.assessment is not None
        finally:
            db.close()

    def test_headache_pathway_complete_lifecycle(self):
        db = SessionLocal()
        try:
            res = consultation_engine.start_session(db, language="hinglish", chief_complaint="Sar me dard hai")
            sid = res.session_id
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "headache_onset_duration"

            res = consultation_engine.process_user_message(db, sid, "Kal subah se dheere dheere shuru hua")
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "headache_location_severity"

            res = consultation_engine.process_user_message(db, sid, "Forehead aur maathe par hai, 5 out of 10")
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "headache_associated"

            res = consultation_engine.process_user_message(db, sid, "Thoda screen fatigue aur neend na aane ki wajah se")
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "headache_neurological_warning"

            res = consultation_engine.process_user_message(db, sid, "Gardan me koi jakdan nahi hai, haath pair theek hain")
            assert res.state == ConversationState.ASSESSMENT
            assert res.assessment is not None
        finally:
            db.close()

    def test_abdominal_pain_pathway_complete_lifecycle(self):
        db = SessionLocal()
        try:
            res = consultation_engine.start_session(db, language="hinglish", chief_complaint="Pet dard ho raha hai")
            sid = res.session_id
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "abd_location_duration"

            res = consultation_engine.process_user_message(db, sid, "Upar pet me jalan hai kal raat khane ke baad se")
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "abd_nature_pain"

            res = consultation_engine.process_user_message(db, sid, "Khatti dakar aur acidity jaisi jalan ho rahi hai")
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "abd_digestive_associated"

            res = consultation_engine.process_user_message(db, sid, "Ulti nahi hui hai, stools normal hain")
            assert res.state == ConversationState.FOLLOW_UP
            assert res.next_question.id == "abd_warning_signs"

            res = consultation_engine.process_user_message(db, sid, "Pet sakht nahi hai, koi khoon nahi aaya")
            assert res.state == ConversationState.ASSESSMENT
            assert res.assessment is not None
        finally:
            db.close()

    def test_skipping_preanswered_questions_in_cough(self):
        # User says upfront: "I have had a dry cough for 4 days"
        # Duration and cough type are already known!
        collected = {
            "duration": "4 days",
            "dry_cough": True,
        }
        next_q = questioning_engine.get_next_question(
            pathway="cough",
            asked_question_ids=[],
            collected_data=collected,
            language="en",
        )
        # Should skip cough_duration (Q1) and proceed
        assert next_q is not None
        assert next_q.id in ["cough_type", "cough_associated"]

    def test_emergency_interruption_during_fever_consultation(self):
        db = SessionLocal()
        try:
            res = consultation_engine.start_session(db, language="hinglish", chief_complaint="Halka bukhar hai")
            sid = res.session_id
            assert res.state == ConversationState.FOLLOW_UP

            # During turn 2, user suddenly reports acute emergency warning
            res_emergency = consultation_engine.process_user_message(
                db, sid, "Achanak seene me bahut tez dard ho raha hai aur baye haath me dard ja raha hai"
            )
            assert res_emergency.state == ConversationState.ESCALATED
            assert res_emergency.safety_status.is_emergency is True
            assert res_emergency.next_question is None
            assert "112" in res_emergency.assistant_message
            assert res_emergency.is_complete is True
        finally:
            db.close()


# ============================================================================
# 2. SAFETY CONTEXT HANDLING TESTS
# ============================================================================

class TestSafetyContextHandling:
    def test_negation_in_english_and_hindi(self):
        # English
        res_en1 = safety_engine.evaluate("I have a bad cold, but definitely no chest pain and no breathing problems")
        assert res_en1.is_emergency is False

        res_en2 = safety_engine.evaluate("Patient denies loss of consciousness or shortness of breath")
        assert res_en2.is_emergency is False

        # Hinglish
        res_hi1 = safety_engine.evaluate("Mujhe bukhar hai par chhati me dard bilkul nahi hai")
        assert res_hi1.is_emergency is False

        # Devanagari Hindi
        res_hi2 = safety_engine.evaluate("मुझे खांसी और बुखार है लेकिन सीने में दर्द नहीं है")
        assert res_hi2.is_emergency is False

    def test_past_versus_current_symptoms(self):
        # Past episode resolved long ago
        res_past1 = safety_engine.evaluate("I had chest pain last year, but today I only have a sore throat")
        assert res_past1.is_emergency is False
        assert res_past1.is_historical is True

        res_past2 = safety_engine.evaluate("Pichle mahine behosh ho gaya tha, abhi sirf halka sar dard hai")
        assert res_past2.is_emergency is False
        assert res_past2.is_historical is True

    def test_resolved_versus_ongoing_symptoms(self):
        # Explicitly resolved symptom: triggers clarification prompt to verify patient safety
        res_resolved = safety_engine.evaluate(
            "I had severe chest pain earlier, but it is completely resolved now and I have no pain",
            language="en"
        )
        assert res_resolved.is_emergency is False
        assert res_resolved.is_ambiguous is True
        assert res_resolved.clarification_prompt is not None
        assert "resolved" in res_resolved.clarification_prompt.lower() or "stopped" in res_resolved.clarification_prompt.lower()

        # Ongoing symptom: triggers immediate emergency
        res_ongoing = safety_engine.evaluate("I had chest pain earlier and it is still hurting right now")
        assert res_ongoing.is_emergency is True

    def test_symptoms_belonging_to_another_person(self):
        # 1. Neighbor had heart attack last year (historical + third party)
        res_neighbor = safety_engine.evaluate("My neighbor had a heart attack last month, but I just have fever")
        assert res_neighbor.is_emergency is False

        # 2. Other person active emergency / unclear ownership: must clarify
        res_father = safety_engine.evaluate("My father is having severe chest pain right now")
        assert res_father.is_emergency is False
        assert res_father.is_ambiguous is True
        assert res_father.is_other_person is True
        assert res_father.clarification_prompt is not None

        # 3. Hinglish dost mention
        res_dost = safety_engine.evaluate("Mere dost ko chhati me tez dard ho raha hai")
        assert res_dost.is_ambiguous is True
        assert res_dost.is_other_person is True

    def test_multiple_people_in_single_message(self):
        # User mentions another person's issue alongside their own symptom
        res_multi = safety_engine.evaluate("My grandfather had severe chest pain, but I am feeling headache")
        # Ownership of the chest pain requires safety clarification
        assert res_multi.is_ambiguous is True
        assert res_multi.clarification_prompt is not None

    def test_uncertainty_and_ambiguity(self):
        res_ambiguous = safety_engine.evaluate("maybe chest pain or gas, not sure if severe pressure")
        assert res_ambiguous.is_emergency is False
        assert res_ambiguous.is_ambiguous is True
        assert res_ambiguous.clarification_prompt is not None


# ============================================================================
# 3. MEDICAL ASSESSMENT GENERATION AUDIT TESTS
# ============================================================================

class TestAssessmentAudit:
    def test_single_nonspecific_symptom_not_forced_into_disease(self):
        # User only reported "headache" with zero duration and no other context
        assessment = assessment_engine.generate_assessment(
            chief_complaint="Sar dard",
            pathway="headache",
            detected_symptoms=["headache"],
            collected_data={},
            follow_up_answers={},
            red_flags_identified=[],
            is_escalated=False,
        )

        # Must NOT force "Migraine without Aura" or similar
        explanation_titles = [e.title for e in assessment.potential_explanations]
        assert not any("Migraine" in t for t in explanation_titles)
        assert any("Undifferentiated" in t for t in explanation_titles)

    def test_no_invented_probability_percentages(self):
        assessment = assessment_engine.generate_assessment(
            chief_complaint="Bukhar aur badan dard",
            pathway="fever",
            detected_symptoms=["fever", "body_pain"],
            collected_data={"timeline": "2 days", "temperature_reading": "101.5 F"},
            follow_up_answers={"fever_associated": "badan dard"},
            red_flags_identified=[],
            is_escalated=False,
        )

        for exp in assessment.potential_explanations:
            assert "%" not in exp.title
            assert "%" not in exp.reasoning
            assert "%" not in exp.likelihood_context
            assert "probability" not in exp.reasoning.lower()

    def test_fact_vs_interpretation_separation(self):
        assessment = assessment_engine.generate_assessment(
            chief_complaint="Pet dard",
            pathway="abdominal_pain",
            detected_symptoms=["abdominal_pain", "nausea_vomiting"],
            collected_data={"timeline": "1 day"},
            follow_up_answers={"abd_nature_pain": "cramping"},
            red_flags_identified=[],
            is_escalated=False,
        )

        assert "chief_complaint" in assessment.user_reported_facts
        assert "reported_symptoms" in assessment.user_reported_facts
        assert "clinical_interpretations_summary" in assessment.model_dump()
        assert len(assessment.missing_or_uncertain_info) > 0

    def test_no_prescription_medicines_or_dosages(self):
        assessment = assessment_engine.generate_assessment(
            chief_complaint="High fever and severe cough",
            pathway="fever",
            detected_symptoms=["fever", "cough"],
            collected_data={"timeline": "3 days"},
            follow_up_answers={},
            red_flags_identified=[],
            is_escalated=False,
        )

        forbidden_med_words = ["paracetamol", "crocin", "azithromycin", "amoxicillin", "tablet", "mg", "dosage", "dose"]
        full_text = " ".join(assessment.suggested_next_steps + [e.reasoning for e in assessment.potential_explanations]).lower()

        for forbidden in forbidden_med_words:
            assert forbidden not in full_text
