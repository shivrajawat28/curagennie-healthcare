"""Health check router reporting system status, database connectivity, and AI mode."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.config import settings
from app.database import get_db
from app.schemas.health import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse)
def check_health(db: Session = Depends(get_db)):
    db_connected = False
    try:
        db.execute(text("SELECT 1"))
        db_connected = True
    except Exception:
        db_connected = False

    mode = "hybrid_llm" if settings.has_ai_provider else "deterministic_local"

    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        database_connected=db_connected,
        ai_provider_configured=settings.has_ai_provider,
        mode=mode,
        details={
            "zero_key_mode": True,
            "voice_stt_mode": "browser_web_speech_api",
            "voice_tts_mode": "browser_speech_synthesis",
            "database_driver": "sqlite3",
            "supported_languages": ["en", "hi", "hinglish"],
        },
    )
