from pydantic import BaseModel
from typing import Dict, Any


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    environment: str
    database_connected: bool
    ai_provider_configured: bool
    mode: str  # "deterministic_local" | "hybrid_llm"
    details: Dict[str, Any]
