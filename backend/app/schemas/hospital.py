"""Pydantic schemas for hospital discovery and appointment enquiry prototypes."""

from typing import List, Optional
from pydantic import BaseModel, Field


class HospitalResponse(BaseModel):
    id: str
    name: str
    hospital_type: str  # "Multi-specialty Hospital", "Government Medical Center", "Specialized Care"
    city: str
    address: str
    emergency_24x7: bool = True
    icu_available: bool = True
    helpline: str
    ambulance_phone: str = "108"
    departments: List[str]
    accreditation: str = "NABH / NABL Accredited (Illustrative Prototype)"
    rating: str = "4.8"


class HospitalListResponse(BaseModel):
    total: int
    hospitals: List[HospitalResponse]
    cities: List[str]
    departments: List[str]


class AppointmentEnquiryRequest(BaseModel):
    doctor_id: Optional[str] = None
    hospital_id: Optional[str] = None
    patient_name: str = Field(..., min_length=2)
    contact_phone: str = Field(..., min_length=10)
    preferred_mode: str = Field(default="teleconsult", description="'teleconsult' or 'in-person'")
    consultation_session_id: Optional[str] = None
    notes: Optional[str] = None


class AppointmentEnquiryResponse(BaseModel):
    enquiry_id: str
    status: str = "received"
    message: str
    provider_name: str
    preferred_mode: str
    is_demo: bool = True
    notice: str = (
        "Illustrative Prototype: This request simulates the appointment enquiry flow. "
        "In production, this securely connects to verified provider scheduling systems."
    )
