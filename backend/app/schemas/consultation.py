from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, description="Message text or voice transcript")
    audio_transcript_raw: Optional[str] = None
    language: Optional[str] = "hinglish"


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime


class ConsultationStartRequest(BaseModel):
    language: str = Field(default="hinglish", description="'en', 'hi', or 'hinglish'")
    chief_complaint: Optional[str] = None


class ConsultationResponse(BaseModel):
    id: str
    created_at: datetime
    language: str
    chief_complaint: str
    stage: str
    risk_level: str
    is_emergency: bool
    welcome_message: Optional[str] = None
    messages: List[MessageResponse] = []
    summary: Optional[Dict[str, Any]] = None
