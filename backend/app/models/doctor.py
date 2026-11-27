"""SQLAlchemy ORM model for doctors and clinic profiles."""

from sqlalchemy import Column, String, Integer, Boolean
from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(String(36), primary_key=True)
    name = Column(String(128), nullable=False)
    specialty = Column(String(128), nullable=False)
    qualification = Column(String(128), default="MBBS", nullable=False)
    experience_years = Column(Integer, default=5, nullable=False)
    hospital_or_clinic = Column(String(255), nullable=False)
    city = Column(String(64), nullable=False)
    languages = Column(String(128), default="Hindi, English", nullable=False)
    teleconsult_available = Column(Boolean, default=True, nullable=False)
    in_person_available = Column(Boolean, default=True, nullable=False)
    fee_inr = Column(Integer, default=500, nullable=False)
    rating = Column(String(8), default="4.8", nullable=False)
