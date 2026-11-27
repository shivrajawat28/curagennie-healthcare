from pydantic import BaseModel
from typing import List, Optional


class DoctorResponse(BaseModel):
    id: str
    name: str
    specialty: str
    qualification: str
    experience_years: int
    hospital_or_clinic: str
    city: str
    languages: str
    teleconsult_available: bool
    in_person_available: bool
    fee_inr: int
    rating: str


class DoctorListResponse(BaseModel):
    total: int
    doctors: List[DoctorResponse]
    cities: List[str]
    specialties: List[str]
