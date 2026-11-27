"""Tests for Agentic AI voice agent router and plug-and-play hook."""

from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

init_db()
client = TestClient(app)


def test_agent_tools_listing():
    """Verifies that the agent tools endpoint lists pre-wired clinical tools."""
    response = client.get("/api/v1/agent/tools")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["total_tools"] >= 4
    tool_names = [t["name"] for t in data["tools"]]
    assert "check_red_flags" in tool_names
    assert "search_available_doctors" in tool_names
    assert "book_hospital_appointment" in tool_names


def test_agent_chat_endpoint():
    """Verifies the direct HTTP route to query the voice agent."""
    payload = {
        "session_id": "test-agent-sess-1",
        "message": "Mujhe bukhar hai",
        "language": "hinglish",
    }
    response = client.post("/api/v1/agent/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "test-agent-sess-1"
    assert "assistant_reply" in data
    assert "is_emergency" in data
