"""Voice Agent Router (Agentic AI & WebSocket Streaming Endpoints)."""

import json
import logging
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, status
from pydantic import BaseModel

from app.agents.voice_agent import voice_agent

logger = logging.getLogger("curagennie.agent_router")

router = APIRouter(prefix="/agent", tags=["Voice Agent (Agentic AI)"])


class AgentChatPayload(BaseModel):
    session_id: str
    message: str
    language: Optional[str] = "hinglish"
    history: Optional[List[Dict[str, str]]] = []


class AgentChatResponse(BaseModel):
    session_id: str
    assistant_reply: str
    is_emergency: bool
    tools_called: List[Any]
    agent_active: bool
    metadata: Dict[str, Any]


@router.post("/chat", response_model=AgentChatResponse)
async def chat_with_voice_agent(payload: AgentChatPayload):
    """Direct HTTP route to query your Agentic AI voice assistant.

    Connect your frontend or external voice orchestrators here.
    """
    result = await voice_agent.process_voice_turn(
        session_id=payload.session_id,
        user_speech_text=payload.message,
        language=payload.language or "hinglish",
        conversation_history=payload.history,
    )

    return AgentChatResponse(
        session_id=payload.session_id,
        assistant_reply=result.get("assistant_reply", ""),
        is_emergency=result.get("is_emergency", False),
        tools_called=result.get("tools_called", []),
        agent_active=result.get("agent_active", False),
        metadata=result.get("metadata", {}),
    )


@router.get("/tools")
def list_agent_tools():
    """Returns the list of clinical tools your future agent has access to."""
    return {
        "status": "ready",
        "total_tools": len(voice_agent.get_available_tools()),
        "tools": voice_agent.get_available_tools(),
    }


@router.websocket("/ws/{session_id}")
async def voice_agent_websocket(websocket: WebSocket, session_id: str):
    """Bi-directional WebSocket for real-time voice streaming.

    Clients (Web Audio / WebRTC) send audio or text chunks,
    and your agent streams back spoken tokens or audio packets in real time.
    """
    await websocket.accept()
    logger.info(f"WebSocket client connected for session: {session_id}")

    try:
        # Welcome packet
        await websocket.send_json({
            "event": "connected",
            "session_id": session_id,
            "message": "Connected to CuraGennie Agentic Voice Streamer.",
        })

        while True:
            # Receive client voice transcript or audio data
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                user_text = payload.get("text", "")
                language = payload.get("language", "hinglish")
            except Exception:
                user_text = data
                language = "hinglish"

            # Execute turn through your voice agent
            agent_output = await voice_agent.process_voice_turn(
                session_id=session_id,
                user_speech_text=user_text,
                language=language,
            )

            # Stream back response to client
            await websocket.send_json({
                "event": "response",
                "session_id": session_id,
                "data": agent_output,
            })

    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected for session: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket streaming error: {e}")
        try:
            await websocket.close()
        except Exception:
            pass
