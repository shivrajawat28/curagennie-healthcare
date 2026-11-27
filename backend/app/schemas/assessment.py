"""Pydantic schemas for structured clinical assessment results."""

from typing import List, Optional
from pydantic import BaseModel, Field


class ClinicalExplanation(BaseModel):
    title: str = Field(..., description="Non-diagnostic potential clinical consideration")
    reasoning: str = Field(..., description="Why this may be relevant based on reported symptoms")
    likelihood_context: str = Field(default="Possible outpatient consideration", description="Cautious framing")


class AssessmentResponse(BaseModel):
    main_concern: str
    reported_symptoms: List[str]
    duration_timeline: Optional[str] = None
    follow_up_summary: dict = Field(default_factory=dict)
    missing_or_uncertain_info: List[str] = Field(default_factory=list)
    potential_explanations: List[ClinicalExplanation] = Field(default_factory=list)
    warning_signs_screened: List[str] = Field(default_factory=list)
    red_flags_identified: List[str] = Field(default_factory=list)
    is_escalated: bool = False
    suggested_next_steps: List[str]
    professional_consultation_recommended: bool = True
    disclaimer: str = Field(
        default="This health summary is an educational triage guide and not a confirmed medical diagnosis or prescription. Always consult a qualified physician for clinical evaluation.",
        description="Standard medical disclaimer"
    )
