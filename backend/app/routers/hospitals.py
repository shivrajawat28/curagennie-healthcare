"""Hospitals router providing Indian healthcare facility discovery and appointment enquiry demo."""

import uuid
from typing import Optional, List
from fastapi import APIRouter, Query, status
from app.schemas.hospital import (
    HospitalListResponse,
    HospitalResponse,
    AppointmentEnquiryRequest,
    AppointmentEnquiryResponse,
)

router = APIRouter(prefix="/hospitals", tags=["Hospitals"])

DEMO_HOSPITALS: List[HospitalResponse] = [
    HospitalResponse(
        id="hosp-1",
        name="Apollo Hospitals & Heart Center",
        hospital_type="Multi-specialty Tertiary Care",
        city="Bengaluru",
        address="154/11 Bannerghatta Road, Opposite IIM, Bengaluru, Karnataka",
        emergency_24x7=True,
        icu_available=True,
        helpline="080-26304050",
        ambulance_phone="1066",
        departments=["Cardiology", "Internal Medicine", "Pulmonology", "Emergency & Trauma", "Neurology"],
        accreditation="JCI & NABH Accredited",
        rating="4.9",
    ),
    HospitalResponse(
        id="hosp-2",
        name="All India Institute of Medical Sciences (AIIMS)",
        hospital_type="Premier Government Medical Institute",
        city="Delhi NCR",
        address="Sri Aurobindo Marg, Ansari Nagar, New Delhi",
        emergency_24x7=True,
        icu_available=True,
        helpline="011-26588500",
        ambulance_phone="102",
        departments=["Internal Medicine", "Pediatrics", "Cardiology", "Pulmonology", "Gastroenterology"],
        accreditation="National Apex Center",
        rating="4.9",
    ),
    HospitalResponse(
        id="hosp-3",
        name="Fortis Memorial Research Institute",
        hospital_type="Super-specialty Hospital",
        city="Delhi NCR",
        address="Sector 44, Opposite HUDA City Centre, Gurugram, Haryana",
        emergency_24x7=True,
        icu_available=True,
        helpline="0124-4962200",
        ambulance_phone="105010",
        departments=["Pulmonology", "Cardiology", "Critical Care", "Neurology", "General Medicine"],
        accreditation="NABH & NABL Accredited",
        rating="4.8",
    ),
    HospitalResponse(
        id="hosp-4",
        name="Narayana Institute of Cardiac Sciences",
        hospital_type="Cardiovascular & Multi-specialty",
        city="Bengaluru",
        address="258/A, Bommasandra Industrial Area, Anekal Taluk, Bengaluru",
        emergency_24x7=True,
        icu_available=True,
        helpline="080-71222222",
        ambulance_phone="108",
        departments=["Cardiology", "Cardiac Surgery", "Critical Care", "Internal Medicine"],
        accreditation="NABH Accredited",
        rating="4.9",
    ),
    HospitalResponse(
        id="hosp-5",
        name="Rainbow Children's Hospital & Perinatal Center",
        hospital_type="Pediatric & Super-specialty",
        city="Mumbai",
        address="Marol Maroshi Road, Andheri East, Mumbai, Maharashtra",
        emergency_24x7=True,
        icu_available=True,
        helpline="022-68955555",
        ambulance_phone="108",
        departments=["Pediatrics", "Pediatric Intensive Care", "Neonatology", "Child Health"],
        accreditation="NABH Accredited",
        rating="4.8",
    ),
    HospitalResponse(
        id="hosp-6",
        name="SMS Hospital & Medical College",
        hospital_type="Apex Government Teaching Hospital",
        city="Jaipur",
        address="Jawahar Lal Nehru Marg, Ashok Nagar, Jaipur, Rajasthan",
        emergency_24x7=True,
        icu_available=True,
        helpline="0141-2560291",
        ambulance_phone="108",
        departments=["Internal Medicine", "Emergency & Trauma", "Dermatology", "General Surgery"],
        accreditation="Government Medical College",
        rating="4.7",
    ),
]


@router.get("", response_model=HospitalListResponse)
def list_hospitals(
    city: Optional[str] = Query(None, description="Filter by Indian city"),
    department: Optional[str] = Query(None, description="Filter by medical department"),
    emergency_only: bool = Query(False, description="Filter 24x7 Emergency facilities"),
):
    results = DEMO_HOSPITALS

    if city:
        results = [h for h in results if h.city.lower() == city.lower()]
    if department:
        results = [h for h in results if any(department.lower() in d.lower() for d in h.departments)]
    if emergency_only:
        results = [h for h in results if h.emergency_24x7]

    all_cities = sorted(list({h.city for h in DEMO_HOSPITALS}))
    all_depts = sorted(list({d for h in DEMO_HOSPITALS for d in h.departments}))

    return HospitalListResponse(
        total=len(results),
        hospitals=results,
        cities=all_cities,
        departments=all_depts,
    )


@router.post("/enquire", response_model=AppointmentEnquiryResponse, status_code=status.HTTP_201_CREATED)
def submit_appointment_enquiry(payload: AppointmentEnquiryRequest):
    """Handles an illustrative appointment enquiry prototype."""
    enquiry_id = f"enq-{str(uuid.uuid4())[:8]}"

    target_name = "Medical Care Facility"
    if payload.hospital_id:
        h = next((x for x in DEMO_HOSPITALS if x.id == payload.hospital_id), None)
        if h:
            target_name = h.name
    elif payload.doctor_id:
        target_name = f"Clinician ({payload.doctor_id})"

    return AppointmentEnquiryResponse(
        enquiry_id=enquiry_id,
        status="received",
        message=f"Appointment enquiry registered for {payload.patient_name} with {target_name}.",
        provider_name=target_name,
        preferred_mode=payload.preferred_mode,
        is_demo=True,
    )
