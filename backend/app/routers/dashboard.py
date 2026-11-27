"""Dashboard router providing metrics, recent consultations, and healthcare guidance."""

from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.session import ConsultationSession
from app.schemas.dashboard import DashboardResponse, RecentConsultationSummary, GuidanceTip

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    # Check if we have sessions in DB, otherwise serve structured illustrative demo sessions
    db_sessions = db.query(ConsultationSession).order_by(ConsultationSession.created_at.desc()).limit(5).all()

    if db_sessions:
        recent = [
            RecentConsultationSummary(
                id=s.id,
                created_at=s.created_at,
                chief_complaint=s.chief_complaint or "General Health Inquiry",
                language=s.language,
                risk_level=s.risk_level,
                stage=s.stage,
                status="Completed" if s.stage in ["triage_complete", "escalated"] else "In Progress"
            )
            for s in db_sessions
        ]
        total_consultations = db.query(ConsultationSession).count()
        completed = sum(1 for s in db_sessions if s.stage in ["triage_complete", "escalated"])
    else:
        now = datetime.now(timezone.utc)
        recent = [
            RecentConsultationSummary(
                id="c-demo-101",
                created_at=now - timedelta(hours=3),
                chief_complaint="Tez bukhar aur sar me dard (High fever & headache for 2 days)",
                language="Hinglish",
                risk_level="medium",
                stage="triage_complete",
                status="Completed"
            ),
            RecentConsultationSummary(
                id="c-demo-102",
                created_at=now - timedelta(days=1, hours=5),
                chief_complaint="Persistent dry cough and mild throat irritation",
                language="English",
                risk_level="low",
                stage="triage_complete",
                status="Completed"
            ),
            RecentConsultationSummary(
                id="c-demo-103",
                created_at=now - timedelta(days=3),
                chief_complaint="Acidity aur pet me jalan khane ke baad",
                language="Hindi / Hinglish",
                risk_level="low",
                stage="triage_complete",
                status="Completed"
            )
        ]
        total_consultations = 3
        completed = 3

    guidance = [
        GuidanceTip(
            id="tip-1",
            title="Dengue & Viral Fever Season Advisory",
            summary="Watch out for high fever with retro-orbital pain, severe platelet drop warnings, or dehydration signs.",
            tag="Preventive Care",
            action_text="Learn warning signs"
        ),
        GuidanceTip(
            id="tip-2",
            title="When to visit an Emergency Department",
            summary="Radiating chest tightness, sudden shortness of breath, slurred speech, or blue lips require immediate emergency care (Call 112).",
            tag="Emergency Protocol",
            action_text="Read emergency red-flags"
        ),
        GuidanceTip(
            id="tip-3",
            title="Voice Consultation Best Practice",
            summary="Speak clearly in English, Hindi or everyday Hinglish. CuraGennie automatically standardizes symptoms and checks warning signs.",
            tag="Voice Feature",
            action_text="Try voice demo"
        )
    ]

    return DashboardResponse(
        welcome_message="Namaste! How can CuraGennie assist with your health today?",
        user_name="Shiv Rajawat",
        stats={
            "total_consultations": total_consultations,
            "completed_consultations": completed,
            "verified_doctors_available": 18,
            "emergency_escalation_ready": True,
        },
        voice_assistant_ready=True,
        recent_consultations=recent,
        guidance_tips=guidance
    )
