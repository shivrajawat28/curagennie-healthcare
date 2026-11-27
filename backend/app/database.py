"""SQLite database configuration and session management via SQLAlchemy."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Ensure sqlite directory exists if file-based
db_url = settings.database_url
if db_url.startswith("sqlite:///") and not db_url.startswith("sqlite:///:memory:"):
    db_path = db_url.replace("sqlite:///", "")
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

# SQLite specific connect args for thread safety with FastAPI
connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

engine = create_engine(
    db_url,
    connect_args=connect_args,
    echo=settings.debug and settings.app_env == "development",
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that yields a database session and safely closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all registered tables."""
    # Import all models to register them on Base.metadata
    from app.models import session as _s, doctor as _d  # noqa: F401
    Base.metadata.create_all(bind=engine)
