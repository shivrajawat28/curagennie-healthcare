"""CuraGennie Voice Agent (Agentic AI Integration).

This file is your dedicated plug-and-play entrypoint for building your future Agentic AI voice assistant.
Whenever you develop your Agentic AI (using LangGraph, AutoGen, CrewAI, Gemini Multimodal Live, or custom LLM agents),
you only need to write your logic inside `process_voice_turn` in this file.

The rest of CuraGennie (Frontend Voice Waveform, STT/TTS, Consultation UI, Database, Doctor/Hospital APIs)
is ALREADY wired to listen to this file!
"""

import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger("curagennie.voice_agent")


class CuraGennieVoiceAgent:
    """Agentic AI handler for autonomous clinical voice conversations and tool executions."""

    def __init__(self, model_name: str = "gemini-1.5-pro"):
        self.model_name = model_name
        self.is_enabled = False  # Set to True when you want the agent to take over responses

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Pre-defined clinical tool schemas ready to be used by your agent's tool-calling engine."""
        return [
            {
                "name": "check_red_flags",
                "description": "Screens patient reported symptoms for acute cardiac, stroke, or respiratory red flags.",
                "parameters": {"symptoms": "list of reported symptom strings"},
            },
            {
                "name": "search_available_doctors",
                "description": "Finds verified specialists currently online or available in user's city.",
                "parameters": {"specialty": "string", "city": "optional string"},
            },
            {
                "name": "book_hospital_appointment",
                "description": "Books an OPD appointment or submits an emergency triage enquiry to a tertiary hospital.",
                "parameters": {"hospital_id": "string", "patient_name": "string", "phone": "string"},
            },
            {
                "name": "generate_prescription_handover",
                "description": "Formats a verified clinical assessment summary for clinician handover.",
                "parameters": {"session_id": "string"},
            },
        ]

    async def process_voice_turn(
        self,
        session_id: str,
        user_speech_text: str,
        language: str = "hinglish",
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """MAIN HOOK: Called whenever the patient speaks or submits a message.

        Whenever you write your agentic code, plug it in here!

        Example integration pattern:
        -----------------------------
        from langchain_google_genai import ChatGoogleGenerativeAI
        agent = create_react_agent(llm, tools=self.get_available_tools())
        result = await agent.ainvoke({"input": user_speech_text, "chat_history": conversation_history})
        return {
            "assistant_reply": result["output"],
            "is_emergency": False,
            "tools_called": result.get("intermediate_steps", []),
        }
        """
        logger.info(f"Voice Agent received input: '{user_speech_text}' for session: {session_id}")

        # Default fallback response until you activate your custom LLM agent:
        return {
            "agent_active": self.is_enabled,
            "assistant_reply": (
                f"नमस्ते! I am CuraGennie's Agentic AI companion. "
                f"I received your message: '{user_speech_text}'. "
                f"Plug your LangGraph/Gemini agent logic directly into app/agents/voice_agent.py."
            ),
            "is_emergency": False,
            "tools_called": [],
            "metadata": {
                "session_id": session_id,
                "language": language,
                "model": self.model_name,
            },
        }


# Global singleton instance ready to be imported across the app
voice_agent = CuraGennieVoiceAgent()
