from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RecentConsultationSummary(BaseModel):
    id: str
    created_at: datetime
    chief_complaint: str
    language: str
    risk_level: str
    stage: str
    status: str


class GuidanceTip(BaseModel):
    id: str
    title: str
    summary: str
    tag: str
    action_text: Optional[str] = None


class DashboardResponse(BaseModel):
    welcome_message: str
    user_name: str
    stats: dict
    voice_assistant_ready: bool
    recent_consultations: List[RecentConsultationSummary]
    guidance_tips: List[GuidanceTip]
