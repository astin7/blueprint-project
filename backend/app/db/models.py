from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key = True, index = True)
    raw_text = Column(Text, nullable = False)
    cleaned_text = Column(Text)
    channel = Column(String(50))
    sender_info = Column(String(255))
    extracted_urls = Column(Text)
    created_at = Column(TIMESTAMP, server_default = func.now())

    detection = relationship("Detection", back_populates = "message", uselist = False, cascade = "all, delete-orphan")
    feedback_items = relationship("Feedback", back_populates = "message", cascade = "all, delete-orphan")


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key = True, index = True)
    message_id = Column(Integer, ForeignKey("messages.id", ondelete = "CASCADE"), nullable = False)
    is_scam = Column(Boolean, nullable = False)
    confidence = Column(Float, nullable = False)
    scam_type = Column(String(100))
    recommended_action = Column(Text)
    model_version = Column(String(50))
    created_at = Column(TIMESTAMP, server_default = func.now())

    message = relationship("Message", back_populates = "detection")
    reasons = relationship("DetectionReason", back_populates = "detection", cascade = "all, delete-orphan")


class DetectionReason(Base):
    __tablename__ = "detection_reasons"

    id = Column(Integer, primary_key = True, index = True)
    detection_id = Column(Integer, ForeignKey("detections.id", ondelete = "CASCADE"), nullable = False)
    reason = Column(Text, nullable = False)

    detection = relationship("Detection", back_populates = "reasons")


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key = True, index = True)
    message_id = Column(Integer, ForeignKey("messages.id", ondelete = "CASCADE"), nullable = False)
    user_feedback = Column(String(50), nullable = False)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default = func.now())

    message = relationship("Message", back_populates = "feedback_items")