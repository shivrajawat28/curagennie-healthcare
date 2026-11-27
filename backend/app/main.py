"""CuraGennie FastAPI Main Application Entrypoint."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.config import settings
from app.database import init_db
from app.core.exceptions import (
    CuraGennieException,
    curagennie_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from app.routers import health, dashboard, consultations, doctors, hospitals, voice_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("curagennie")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize database schema
    logger.info("Initializing CuraGennie SQLite database...")
    init_db()
    logger.info(f"CuraGennie backend online on port {settings.port} (Environment: {settings.app_env})")
    yield
    # Shutdown
    logger.info("CuraGennie backend shutting down.")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Voice-First AI Healthcare Assistant for India (Zero-key out-of-the-box support)",
    lifespan=lifespan,
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Centralized Exception Handlers
app.add_exception_handler(CuraGennieException, curagennie_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include API Routers under /api/v1 prefix
api_prefix = "/api/v1"
app.include_router(health.router, prefix=api_prefix)
app.include_router(dashboard.router, prefix=api_prefix)
app.include_router(consultations.router, prefix=api_prefix)
app.include_router(doctors.router, prefix=api_prefix)
app.include_router(hospitals.router, prefix=api_prefix)
app.include_router(voice_agent.router, prefix=api_prefix)


@app.get("/")
def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "tagline": "Your health deserves to be heard.",
        "docs_url": "/docs",
        "health_check": f"{api_prefix}/health",
    }
