"""Consultations router handling conversation sessions, live messaging, triage, and history."""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.session import ConsultationSession
from app.schemas.conversation import (
    StartConsultationPayload,
    UserMessagePayload,
    EngineResponse,
    SessionStateDetail,
)
from app.schemas.assessment import AssessmentResponse
from app.schemas.consultation import ConsultationResponse, MessageResponse
from app.services.consultation_engine import consultation_engine

router = APIRouter(prefix="/consultations", tags=["Consultations"])


@router.post("/start", response_model=EngineResponse, status_code=status.HTTP_201_CREATED)
def start_consultation(
    payload: StartConsultationPayload,
    db: Session = Depends(get_db),
):
    """Initializes a new consultation conversation session."""
    return consultation_engine.start_session(
        db=db,
        language=payload.language,
        chief_complaint=payload.chief_complaint,
    )


@router.post("", response_model=EngineResponse, status_code=status.HTTP_201_CREATED)
def start_consultation_legacy(
    payload: StartConsultationPayload,
    db: Session = Depends(get_db),
):
    """Alias for POST /start for backward compatibility."""
    return consultation_engine.start_session(
        db=db,
        language=payload.language,
        chief_complaint=payload.chief_complaint,
    )


@router.post("/{session_id}/message", response_model=EngineResponse)
def send_message(
    session_id: str,
    payload: UserMessagePayload,
    db: Session = Depends(get_db),
):
    """Processes an incoming user message through safety checks and conversation flow."""
    try:
        return consultation_engine.process_user_message(
            db=db,
            session_id=session_id,
            user_text=payload.content,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing consultation message: {str(e)}",
        )


@router.get("/{session_id}", response_model=SessionStateDetail)
def get_consultation_detail(
    session_id: str,
    db: Session = Depends(get_db),
):
    """Retrieves current session state and transcript for resumption or review."""
    try:
        return consultation_engine.get_session_detail(db, session_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{session_id}/assessment", response_model=AssessmentResponse)
def get_consultation_assessment(
    session_id: str,
    db: Session = Depends(get_db),
):
    """Retrieves generated clinical assessment for a completed or escalated session."""
    try:
        detail = consultation_engine.get_session_detail(db, session_id)
        if not detail.assessment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Assessment is not yet available for this session. Complete the intake questions first.",
            )
        return detail.assessment
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{session_id}/complete", response_model=SessionStateDetail)
def complete_consultation(
    session_id: str,
    db: Session = Depends(get_db),
):
    """Marks a consultation session as COMPLETED."""
    try:
        return consultation_engine.complete_session(db, session_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("", response_model=List[ConsultationResponse])
def list_consultations(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Lists historical consultation records."""
    sessions = db.query(ConsultationSession).order_by(ConsultationSession.created_at.desc()).limit(limit).all()

    return [
        ConsultationResponse(
            id=s.id,
            created_at=s.created_at,
            language=s.language,
            chief_complaint=s.chief_complaint or "General Health Consultation",
            stage=s.stage,
            risk_level=s.risk_level,
            is_emergency=s.is_emergency,
            messages=[
                MessageResponse(id=m.id, role=m.role, content=m.content, created_at=m.created_at)
                for m in s.messages
            ],
        )
        for s in sessions
    ]
