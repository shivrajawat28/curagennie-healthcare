"""SQLAlchemy ORM models for consultations and messages."""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class ConsultationSession(Base):
    __tablename__ = "consultation_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
    
    language = Column(String(16), default="hinglish", nullable=False)  # "en", "hi", "hinglish"
    chief_complaint = Column(String(255), default="", nullable=False)
    stage = Column(String(32), default="intake", nullable=False)  # "intake", "follow_up", "triage_complete", "escalated"
    risk_level = Column(String(16), default="low", nullable=False)  # "low", "medium", "high", "emergency"
    follow_up_count = Column(Integer, default=0, nullable=False)
    is_emergency = Column(Boolean, default=False, nullable=False)
    summary_json = Column(Text, default="{}", nullable=False)

    messages = relationship("ConsultationMessage", back_populates="session", cascade="all, delete-orphan")


class ConsultationMessage(Base):
    __tablename__ = "consultation_messages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("consultation_sessions.id"), nullable=False)
    role = Column(String(16), nullable=False)  # "user", "assistant", "system"
    content = Column(Text, nullable=False)
    audio_transcript_raw = Column(Text, nullable=True)
    detected_language = Column(String(16), default="hinglish", nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    session = relationship("ConsultationSession", back_populates="messages")
