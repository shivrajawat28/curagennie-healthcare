"""Integration tests for backend health, dashboard, doctors, and consultations."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

# Initialize database schema for test session
init_db()

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "CuraGennie"
    assert "health_check" in data


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database_connected"] is True
    assert "details" in data
    assert data["details"]["zero_key_mode"] is True


def test_dashboard_endpoint():
    response = client.get("/api/v1/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "welcome_message" in data
    assert "stats" in data
    assert "recent_consultations" in data
    assert len(data["recent_consultations"]) > 0
    assert "guidance_tips" in data


def test_doctors_endpoint():
    response = client.get("/api/v1/doctors")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    assert len(data["doctors"]) > 0
    assert "Bengaluru" in data["cities"]


def test_consultations_list():
    response = client.get("/api/v1/consultations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_start_consultation():
    payload = {
        "language": "hinglish",
        "chief_complaint": "Persistent headache"
    }
    response = client.post("/api/v1/consultations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["language"] == "hinglish"
    assert data["stage"] == "intake"
    assert len(data["messages"]) == 1
