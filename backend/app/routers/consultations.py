"""Consultations router handling consultation lifecycle and history."""

import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.session import ConsultationSession, ConsultationMessage
from app.schemas.consultation import (
    ConsultationResponse,
    ConsultationStartRequest,
    MessageResponse
)

router = APIRouter(prefix="/consultations", tags=["Consultations"])


@router.get("", response_model=List[ConsultationResponse])
def list_consultations(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    sessions = db.query(ConsultationSession).order_by(ConsultationSession.created_at.desc()).limit(limit).all()
    
    if not sessions:
        # Provide clean, illustrative demo consultations until Phase 02 creates live ones
        now = datetime.now(timezone.utc)
        return [
            ConsultationResponse(
                id="c-demo-101",
                created_at=now - timedelta(hours=3),
                language="Hinglish",
                chief_complaint="Tez bukhar aur sar me dard (High fever & headache for 2 days)",
                stage="triage_complete",
                risk_level="medium",
                is_emergency=False,
                welcome_message="Namaste! Aapko kab se bukhar mehsoos ho raha hai?",
                messages=[
                    MessageResponse(
                        id="m-1",
                        role="assistant",
                        content="Namaste! Aapko kab se bukhar aur sar dard mehsoos ho raha hai?",
                        created_at=now - timedelta(hours=3, minutes=5)
                    ),
                    MessageResponse(
                        id="m-2",
                        role="user",
                        content="Mujhe kal raat se tez bukhar hai aur aankho ke peeche dard ho raha hai.",
                        created_at=now - timedelta(hours=3, minutes=4)
                    ),
                    MessageResponse(
                        id="m-3",
                        role="assistant",
                        content="Kya aapko thand lag rahi hai ya sharir par koi laal daane (rashes) dikh rahe hain?",
                        created_at=now - timedelta(hours=3, minutes=3)
                    )
                ],
                summary={
                    "chief_complaint": "Acute Febrile Illness with retro-orbital headache",
                    "duration": "2 days",
                    "risk_assessment": "Moderate risk - viral prodrome / dengue differential",
                    "red_flags_present": False,
                    "recommended_action": "Consult General Physician, complete CBC/platelet count, maintain oral hydration."
                }
            ),
            ConsultationResponse(
                id="c-demo-102",
                created_at=now - timedelta(days=1, hours=5),
                language="English",
                chief_complaint="Persistent dry cough and mild throat irritation",
                stage="triage_complete",
                risk_level="low",
                is_emergency=False,
                welcome_message="Hello, I'm CuraGennie. Please tell me about your cough.",
                messages=[
                    MessageResponse(
                        id="m-4",
                        role="assistant",
                        content="Hello, I'm CuraGennie. How long have you had this cough?",
                        created_at=now - timedelta(days=1, hours=5, minutes=3)
                    ),
                    MessageResponse(
                        id="m-5",
                        role="user",
                        content="It started 4 days ago, mostly a dry tickle in the throat, no fever.",
                        created_at=now - timedelta(days=1, hours=5, minutes=2)
                    )
                ],
                summary={
                    "chief_complaint": "Subacute upper respiratory irritation",
                    "duration": "4 days",
                    "risk_assessment": "Low risk - likely post-viral or allergic pharyngitis",
                    "red_flags_present": False,
                    "recommended_action": "Warm saline gargles, steam inhalation, observe for 3 days."
                }
            ),
            ConsultationResponse(
                id="c-demo-103",
                created_at=now - timedelta(days=3),
                language="Hinglish",
                chief_complaint="Acidity aur pet me jalan khane ke baad",
                stage="triage_complete",
                risk_level="low",
                is_emergency=False,
                welcome_message="Namaste, pet me jalan kis samay zyada hoti hai?",
                messages=[],
                summary={
                    "chief_complaint": "Postprandial dyspepsia and epigastric burning",
                    "duration": "1 week intermittent",
                    "risk_assessment": "Low risk - functional dyspepsia / GERD symptoms",
                    "red_flags_present": False,
                    "recommended_action": "Avoid spicy/late meals, consult physician if symptoms persist beyond 10 days."
                }
            )
        ]

    return [
        ConsultationResponse(
            id=s.id,
            created_at=s.created_at,
            language=s.language,
            chief_complaint=s.chief_complaint,
            stage=s.stage,
            risk_level=s.risk_level,
            is_emergency=s.is_emergency,
            messages=[
                MessageResponse(id=m.id, role=m.role, content=m.content, created_at=m.created_at)
                for m in s.messages
            ]
        )
        for s in sessions
    ]


@router.post("", response_model=ConsultationResponse)
def start_consultation(
    payload: ConsultationStartRequest,
    db: Session = Depends(get_db)
):
    """Creates a new consultation session and returns the initial welcome prompt."""
    welcome_text = (
        "Namaste! Mai CuraGennie hoon, aapka personal health assistant. "
        "Aap apni takleef ya lakshan Hindi, English ya Hinglish me batayein."
        if payload.language in ["hi", "hinglish"]
        else "Hello! I am CuraGennie, your personal health navigation assistant. "
        "Please describe what symptoms or health concerns you are experiencing today."
    )

    new_session = ConsultationSession(
        id=str(uuid.uuid4()),
        language=payload.language,
        chief_complaint=payload.chief_complaint or "",
        stage="intake",
        risk_level="low",
        is_emergency=False
    )
    
    welcome_msg = ConsultationMessage(
        id=str(uuid.uuid4()),
        session_id=new_session.id,
        role="assistant",
        content=welcome_text,
        detected_language=payload.language
    )
    
    db.add(new_session)
    db.add(welcome_msg)
    db.commit()
    db.refresh(new_session)

    return ConsultationResponse(
        id=new_session.id,
        created_at=new_session.created_at,
        language=new_session.language,
        chief_complaint=new_session.chief_complaint,
        stage=new_session.stage,
        risk_level=new_session.risk_level,
        is_emergency=new_session.is_emergency,
        welcome_message=welcome_text,
        messages=[
            MessageResponse(
                id=welcome_msg.id,
                role=welcome_msg.role,
                content=welcome_msg.content,
                created_at=welcome_msg.created_at
            )
        ]
    )
