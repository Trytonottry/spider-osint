# db/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True)
    value = Column(String(255), unique=True, index=True)  # email, domain и т.д.
    type = Column(String(50))  # email, domain, ip, username
    created_at = Column(DateTime, default=datetime.utcnow)
    last_scanned = Column(DateTime, default=datetime.utcnow)

    results = relationship("ScanResult", back_populates="target", cascade="all, delete-orphan")

class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True)
    target_id = Column(Integer, ForeignKey("targets.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    modules_used = Column(String(500))
    data = Column(JSON)  # Полный JSON-результат
    report_pdf = Column(String(500))  # Путь к отчёту
    report_html = Column(String(500))
    suspicious = Column(Boolean, default=False)  # Флаг угрозы

    target = relationship("Target", back_populates="results")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    hashed_password = Column(String(255))
    role = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)