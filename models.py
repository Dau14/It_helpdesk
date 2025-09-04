from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  
    tickets = relationship("Ticket", back_populates="user")
    assets = relationship("Asset", back_populates="user")
    logs = relationship("Log", back_populates="user")

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    status = Column(String, default="open")
    priority = Column(String, default="medium")  
    escalation_level = Column(Integer, default=0)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship("User", back_populates="tickets")

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(String, default="available")
    location = Column(String)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    user = relationship("User", back_populates="assets")

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="logs")