"""Integration tests for hospital discovery and appointment enquiry demo."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_hospitals_all():
    res = client.get("/api/v1/hospitals")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 6
    assert len(data["hospitals"]) >= 6
    assert "Bengaluru" in data["cities"]
    assert "Cardiology" in data["departments"]


def test_filter_hospitals_by_city():
    res = client.get("/api/v1/hospitals?city=Delhi%20NCR")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 2
    for h in data["hospitals"]:
        assert h["city"] == "Delhi NCR"


def test_filter_hospitals_by_department():
    res = client.get("/api/v1/hospitals?department=Pediatrics")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] >= 1
    assert any("Rainbow" in h["name"] or "AIIMS" in h["name"] for h in data["hospitals"])


def test_appointment_enquiry_demo_submission():
    payload = {
        "hospital_id": "hosp-1",
        "patient_name": "Rohan Gupta",
        "contact_phone": "9876543210",
        "preferred_mode": "teleconsult",
        "notes": "Follow-up for persistent cough and throat irritation"
    }
    res = client.post("/api/v1/hospitals/enquire", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert "enquiry_id" in data
    assert data["status"] == "received"
    assert data["is_demo"] is True
    assert "Apollo" in data["provider_name"]
