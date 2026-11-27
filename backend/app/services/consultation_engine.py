"""Core consultation conversation engine orchestrating the state machine,
safety screening, multilingual normalization, follow-up questioning, and persistence.
"""

import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Tuple
from sqlalchemy.orm import Session

from app.models.session import ConsultationSession, ConsultationMessage
from app.schemas.conversation import (
    ConversationState,
    EngineResponse,
    SafetyStatus,
    SessionStateDetail,
)
from app.schemas.assessment import AssessmentResponse
from app.services.symptom_normalizer import symptom_normalizer
from app.services.safety_engine import safety_engine
from app.services.questioning_engine import questioning_engine
from app.services.assessment_engine import assessment_engine


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ConsultationEngine:
    def start_session(
        self,
        db: Session,
        language: str = "hinglish",
        chief_complaint: Optional[str] = None,
    ) -> EngineResponse:
        """Initializes a new consultation session and delivers the welcome prompt."""
        session_id = str(uuid.uuid4())
        lang = language.lower() if language else "hinglish"

        if lang in ["hi", "hinglish"]:
            welcome_msg = (
                "Namaste! Mai CuraGennie hoon, aapka healthcare navigation assistant. "
                "Aap apni takleef ya lakshan Hindi, English ya Hinglish me batayein — "
                "jaise kab se bukhar, sar dard ya koi pareshani mehsoos ho rahi hai."
            )
        else:
            welcome_msg = (
                "Hello! I am CuraGennie, your personal health navigation assistant. "
                "Please describe what symptoms you are experiencing today in your own words, "
                "and how long you have been feeling unwell."
            )

        session = ConsultationSession(
            id=session_id,
            language=lang,
            chief_complaint=chief_complaint or "",
            stage=ConversationState.INTAKE.value,
            risk_level="low",
            is_emergency=False,
            follow_up_count=0,
            summary_json=json.dumps({
                "pathway": "general",
                "asked_question_ids": [],
                "collected_data": {},
                "follow_up_answers": {},
                "detected_symptoms": [],
                "red_flags": [],
            }),
            created_at=utc_now(),
            updated_at=utc_now(),
        )

        initial_message = ConsultationMessage(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role="assistant",
            content=welcome_msg,
            detected_language=lang,
            created_at=utc_now(),
        )

        db.add(session)
        db.add(initial_message)
        db.commit()

        # If user passed initial chief complaint with start payload, process it immediately
        if chief_complaint and chief_complaint.strip():
            return self.process_user_message(db, session_id, chief_complaint)

        return EngineResponse(
            session_id=session_id,
            state=ConversationState.INTAKE,
            assistant_message=welcome_msg,
            next_question=None,
            safety_status=SafetyStatus(is_emergency=False, is_ambiguous=False),
            normalized_symptoms=[],
            assessment=None,
            is_complete=False,
            created_at=session.created_at,
        )

    def process_user_message(
        self,
        db: Session,
        session_id: str,
        user_text: str,
    ) -> EngineResponse:
        """Processes user input through the safety engine, normalization, and state machine."""
        session = db.query(ConsultationSession).filter(ConsultationSession.id == session_id).first()
        if not session:
            raise ValueError(f"Consultation session '{session_id}' not found.")

        # Persist incoming user message
        user_msg_record = ConsultationMessage(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role="user",
            content=user_text,
            detected_language=session.language,
            created_at=utc_now(),
        )
        db.add(user_msg_record)

        # Unpack session memory
        try:
            memory = json.loads(session.summary_json) if session.summary_json else {}
        except Exception:
            memory = {}

        pathway = memory.get("pathway", "general")
        asked_q_ids = memory.get("asked_question_ids", [])
        collected_data = memory.get("collected_data", {})
        follow_up_answers = memory.get("follow_up_answers", {})
        detected_symptoms = memory.get("detected_symptoms", [])
        red_flags = memory.get("red_flags", [])

        # STEP 1: SAFETY CHECK (HIGHEST PRIORITY - ALWAYS RUNS FIRST)
        safety_result = safety_engine.evaluate(user_text, language=session.language)

        if safety_result.is_emergency:
            # Immediate Emergency Escalation
            session.stage = ConversationState.ESCALATED.value
            session.is_emergency = True
            session.risk_level = "emergency"
            red_flags.extend(safety_result.triggered_flags)
            memory["red_flags"] = list(set(red_flags))
            session.summary_json = json.dumps(memory)
            session.updated_at = utc_now()

            # Generate immediate emergency assessment
            assessment = assessment_engine.generate_assessment(
                chief_complaint=session.chief_complaint or user_text,
                pathway=pathway,
                detected_symptoms=detected_symptoms,
                collected_data=collected_data,
                follow_up_answers=follow_up_answers,
                red_flags_identified=memory["red_flags"],
                is_escalated=True,
            )

            assistant_msg = safety_result.emergency_message or (
                "⚠️ Emergency Warning: Urgent medical symptoms identified. Call 112 immediately."
            )

            asst_msg_record = ConsultationMessage(
                id=str(uuid.uuid4()),
                session_id=session_id,
                role="assistant",
                content=assistant_msg,
                detected_language=session.language,
                created_at=utc_now(),
            )
            db.add(asst_msg_record)
            db.commit()

            return EngineResponse(
                session_id=session_id,
                state=ConversationState.ESCALATED,
                assistant_message=assistant_msg,
                next_question=None,
                safety_status=SafetyStatus(
                    is_emergency=True,
                    is_ambiguous=False,
                    red_flags_detected=safety_result.triggered_flags,
                    action_required="IMMEDIATE_EMERGENCY_ESCALATION",
                ),
                normalized_symptoms=detected_symptoms,
                assessment=assessment,
                is_complete=True,
                created_at=asst_msg_record.created_at,
            )

        if safety_result.is_ambiguous and safety_result.clarification_prompt:
            # Ambiguous red-flag requires clarification prompt without escalating or dismissing
            assistant_msg = safety_result.clarification_prompt
            asst_msg_record = ConsultationMessage(
                id=str(uuid.uuid4()),
                session_id=session_id,
                role="assistant",
                content=assistant_msg,
                detected_language=session.language,
                created_at=utc_now(),
            )
            db.add(asst_msg_record)
            db.commit()

            return EngineResponse(
                session_id=session_id,
                state=ConversationState(session.stage),
                assistant_message=assistant_msg,
                next_question=None,
                safety_status=SafetyStatus(
                    is_emergency=False,
                    is_ambiguous=True,
                    red_flags_detected=safety_result.triggered_flags,
                    action_required="CLARIFY_EMERGENCY_SYMPTOM",
                ),
                normalized_symptoms=detected_symptoms,
                assessment=None,
                is_complete=False,
                created_at=asst_msg_record.created_at,
            )

        # STEP 2: SYMPTOM EXTRACTION & NORMALIZATION
        extraction = symptom_normalizer.normalize(user_text)

        # Merge extracted symptoms
        for sym in extraction.detected_symptoms:
            if sym not in detected_symptoms:
                detected_symptoms.append(sym)

        # Update timeline, temperature, severity in memory
        if extraction.timeline:
            collected_data["timeline"] = extraction.timeline
        if extraction.temperature_reading:
            collected_data["temperature_reading"] = extraction.temperature_reading
        if extraction.severity_cue:
            collected_data["severity_cue"] = extraction.severity_cue

        # If we were waiting for an answer to a previously asked question, store it
        if asked_q_ids:
            last_asked_id = asked_q_ids[-1]
            follow_up_answers[last_asked_id] = user_text

        # Set or refine primary pathway
        if not session.chief_complaint or pathway == "general":
            session.chief_complaint = session.chief_complaint or user_text
            pathway = symptom_normalizer.determine_primary_pathway(detected_symptoms)

        # STEP 3: CONSULTATION STATE TRANSITIONS & FOLLOW-UP QUESTIONS
        # If in INTAKE or FOLLOW_UP, ask the next question up to MAX_QUESTIONS (4)
        next_q = questioning_engine.get_next_question(
            pathway=pathway,
            asked_question_ids=asked_q_ids,
            collected_data=collected_data,
            language=session.language,
        )

        if next_q:
            # We have a relevant question to ask
            session.stage = ConversationState.FOLLOW_UP.value
            asked_q_ids.append(next_q.id)
            session.follow_up_count = len(asked_q_ids)

            memory["pathway"] = pathway
            memory["asked_question_ids"] = asked_q_ids
            memory["collected_data"] = collected_data
            memory["follow_up_answers"] = follow_up_answers
            memory["detected_symptoms"] = detected_symptoms
            session.summary_json = json.dumps(memory)
            session.updated_at = utc_now()

            assistant_msg = next_q.text

            asst_msg_record = ConsultationMessage(
                id=str(uuid.uuid4()),
                session_id=session_id,
                role="assistant",
                content=assistant_msg,
                detected_language=session.language,
                created_at=utc_now(),
            )
            db.add(asst_msg_record)
            db.commit()

            return EngineResponse(
                session_id=session_id,
                state=ConversationState.FOLLOW_UP,
                assistant_message=assistant_msg,
                next_question=next_q,
                safety_status=SafetyStatus(is_emergency=False, is_ambiguous=False),
                normalized_symptoms=detected_symptoms,
                assessment=None,
                is_complete=False,
                created_at=asst_msg_record.created_at,
            )

        # STEP 4: ALL QUESTIONS ANSWERED OR MAX REACHED -> GENERATE ASSESSMENT
        session.stage = ConversationState.ASSESSMENT.value
        risk = "medium" if pathway in ["fever", "abdominal_pain"] else "low"
        session.risk_level = risk

        assessment = assessment_engine.generate_assessment(
            chief_complaint=session.chief_complaint or user_text,
            pathway=pathway,
            detected_symptoms=detected_symptoms,
            collected_data=collected_data,
            follow_up_answers=follow_up_answers,
            red_flags_identified=red_flags,
            is_escalated=False,
        )

        memory["pathway"] = pathway
        memory["asked_question_ids"] = asked_q_ids
        memory["collected_data"] = collected_data
        memory["follow_up_answers"] = follow_up_answers
        memory["detected_symptoms"] = detected_symptoms
        memory["assessment"] = assessment.model_dump()
        session.summary_json = json.dumps(memory)
        session.updated_at = utc_now()

        if session.language in ["hi", "hinglish"]:
            summary_intro = (
                "Dhanyawaad! Aapki jankari ke aadhar par maine aapka health assessment summary taiyar kar liya hai. "
                "Kripya dhyan dein ki yeh aupcharik diagnosis ya prescription nahi hai, balki aapki dekhbhaal ke liye ek margdarshak (guidance) hai."
            )
        else:
            summary_intro = (
                "Thank you. Based on the symptoms and details you provided, I have prepared your structured clinical triage assessment. "
                "Please remember that this is educational health guidance and not a confirmed diagnosis or medication prescription."
            )

        asst_msg_record = ConsultationMessage(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role="assistant",
            content=summary_intro,
            detected_language=session.language,
            created_at=utc_now(),
        )
        db.add(asst_msg_record)
        db.commit()

        return EngineResponse(
            session_id=session_id,
            state=ConversationState.ASSESSMENT,
            assistant_message=summary_intro,
            next_question=None,
            safety_status=SafetyStatus(is_emergency=False, is_ambiguous=False),
            normalized_symptoms=detected_symptoms,
            assessment=assessment,
            is_complete=True,
            created_at=asst_msg_record.created_at,
        )

    def get_session_detail(self, db: Session, session_id: str) -> SessionStateDetail:
        """Retrieves complete session history and state for resumption."""
        session = db.query(ConsultationSession).filter(ConsultationSession.id == session_id).first()
        if not session:
            raise ValueError(f"Consultation session '{session_id}' not found.")

        try:
            memory = json.loads(session.summary_json) if session.summary_json else {}
        except Exception:
            memory = {}

        assessment_data = memory.get("assessment")
        assessment = AssessmentResponse(**assessment_data) if assessment_data else None

        messages = [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat(),
            }
            for m in session.messages
        ]

        return SessionStateDetail(
            session_id=session.id,
            state=ConversationState(session.stage),
            language=session.language,
            chief_complaint=session.chief_complaint,
            pathway=memory.get("pathway", "general"),
            follow_up_count=session.follow_up_count,
            is_emergency=session.is_emergency,
            created_at=session.created_at,
            updated_at=session.updated_at,
            collected_data=memory.get("collected_data", {}),
            messages=messages,
            assessment=assessment,
        )

    def complete_session(self, db: Session, session_id: str) -> SessionStateDetail:
        """Marks a consultation as COMPLETED."""
        session = db.query(ConsultationSession).filter(ConsultationSession.id == session_id).first()
        if not session:
            raise ValueError(f"Consultation session '{session_id}' not found.")

        session.stage = ConversationState.COMPLETED.value
        session.updated_at = utc_now()
        db.commit()

        return self.get_session_detail(db, session_id)


consultation_engine = ConsultationEngine()
