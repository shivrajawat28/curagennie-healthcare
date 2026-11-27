"""Pydantic schemas for the healthcare conversation engine."""

from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.assessment import AssessmentResponse


class ConversationState(str, Enum):
    INITIAL = "INITIAL"
    INTAKE = "INTAKE"
    SAFETY_CHECK = "SAFETY_CHECK"
    FOLLOW_UP = "FOLLOW_UP"
    ASSESSMENT = "ASSESSMENT"
    COMPLETED = "COMPLETED"
    ESCALATED = "ESCALATED"


class QuestionDetail(BaseModel):
    id: str
    key: str
    text: str
    category: str
    question_index: int = 1
    total_questions: int = 4


class SafetyStatus(BaseModel):
    is_emergency: bool = False
    is_ambiguous: bool = False
    red_flags_detected: List[str] = Field(default_factory=list)
    action_required: Optional[str] = None
    emergency_contact: str = "112"


class StartConsultationPayload(BaseModel):
    language: str = Field(default="hinglish", description="'en', 'hi', or 'hinglish'")
    chief_complaint: Optional[str] = None


class UserMessagePayload(BaseModel):
    content: str = Field(..., min_length=1, description="Patient message text")
    language: Optional[str] = None


class EngineResponse(BaseModel):
    session_id: str
    state: ConversationState
    assistant_message: str
    next_question: Optional[QuestionDetail] = None
    safety_status: SafetyStatus
    normalized_symptoms: List[str] = Field(default_factory=list)
    assessment: Optional[AssessmentResponse] = None
    is_complete: bool = False
    created_at: datetime


class SessionStateDetail(BaseModel):
    session_id: str
    state: ConversationState
    language: str
    chief_complaint: str
    pathway: str
    follow_up_count: int
    is_emergency: bool
    created_at: datetime
    updated_at: datetime
    collected_data: Dict[str, Any] = Field(default_factory=dict)
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    assessment: Optional[AssessmentResponse] = None
