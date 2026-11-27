"""Application configuration management with Pydantic Settings."""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CuraGennie"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = True
    
    host: str = "0.0.0.0"
    port: int = 8001
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"
    
    database_url: str = "sqlite:///./curagennie.db"
    
    # Optional external AI providers (none required for core functionality)
    gemini_api_key: str = ""
    openai_api_key: str = ""

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def has_ai_provider(self) -> bool:
        return bool(self.gemini_api_key or self.openai_api_key)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
