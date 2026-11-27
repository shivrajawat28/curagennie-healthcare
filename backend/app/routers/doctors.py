"""Doctors router providing Indian verified clinician directory and teleconsult discovery."""

from typing import Optional
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorListResponse, DoctorResponse

router = APIRouter(prefix="/doctors", tags=["Doctors"])

DEMO_DOCTORS = [
    DoctorResponse(
        id="doc-1",
        name="Dr. Priya Sharma",
        specialty="General Physician & Internal Medicine",
        qualification="MBBS, MD (Medicine) - AIIMS New Delhi",
        experience_years=12,
        hospital_or_clinic="Apollo Clinic / Medicity",
        city="Bengaluru",
        languages="Hindi, English, Kannada",
        teleconsult_available=True,
        in_person_available=True,
        fee_inr=600,
        rating="4.9"
    ),
    DoctorResponse(
        id="doc-2",
        name="Dr. Rajesh Verma",
        specialty="Pulmonology & Chest Medicine",
        qualification="MBBS, DNB (Respiratory Diseases)",
        experience_years=15,
        hospital_or_clinic="Fortis Healthcare",
        city="Delhi NCR",
        languages="Hindi, English, Punjabi",
        teleconsult_available=True,
        in_person_available=True,
        fee_inr=800,
        rating="4.8"
    ),
    DoctorResponse(
        id="doc-3",
        name="Dr. Ananya Mukherjee",
        specialty="Pediatrics & Child Health",
        qualification="MBBS, MD (Pediatrics)",
        experience_years=9,
        hospital_or_clinic="Rainbow Children's Hospital",
        city="Mumbai",
        languages="Hindi, English, Bengali, Marathi",
        teleconsult_available=True,
        in_person_available=True,
        fee_inr=700,
        rating="4.9"
    ),
    DoctorResponse(
        id="doc-4",
        name="Dr. Suresh Patel",
        specialty="Cardiology & Preventive Cardiology",
        qualification="MBBS, MD, DM (Cardiology)",
        experience_years=18,
        hospital_or_clinic="Narayana Health",
        city="Bengaluru",
        languages="Hindi, English, Gujarati",
        teleconsult_available=True,
        in_person_available=True,
        fee_inr=1000,
        rating="4.9"
    ),
    DoctorResponse(
        id="doc-5",
        name="Dr. Meenakshi Sundaram",
        specialty="Gastroenterology & Hepatology",
        qualification="MBBS, MD, DM (Gastro)",
        experience_years=11,
        hospital_or_clinic="Manipal Hospital",
        city="Chennai",
        languages="English, Tamil, Hindi",
        teleconsult_available=True,
        in_person_available=True,
        fee_inr=750,
        rating="4.7"
    ),
    DoctorResponse(
        id="doc-6",
        name="Dr. Vikram Chauhan",
        specialty="Dermatology & Venereology",
        qualification="MBBS, DVD, MD",
        experience_years=8,
        hospital_or_clinic="Skin & Wellness Clinic",
        city="Jaipur",
        languages="Hindi, English, Rajasthani",
        teleconsult_available=True,
        in_person_available=True,
        fee_inr=500,
        rating="4.8"
    )
]


@router.get("", response_model=DoctorListResponse)
def list_doctors(
    city: Optional[str] = Query(None, description="Filter by Indian city"),
    specialty: Optional[str] = Query(None, description="Filter by medical specialty"),
    teleconsult_only: bool = Query(False, description="Filter teleconsult-enabled clinicians"),
    db: Session = Depends(get_db)
):
    results = DEMO_DOCTORS

    if city:
        results = [d for d in results if d.city.lower() == city.lower()]
    if specialty:
        results = [d for d in results if specialty.lower() in d.specialty.lower()]
    if teleconsult_only:
        results = [d for d in results if d.teleconsult_available]

    all_cities = sorted(list({d.city for d in DEMO_DOCTORS}))
    all_specialties = sorted(list({d.specialty for d in DEMO_DOCTORS}))

    return DoctorListResponse(
        total=len(results),
        doctors=results,
        cities=all_cities,
        specialties=all_specialties
    )
