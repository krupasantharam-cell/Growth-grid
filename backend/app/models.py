import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
)
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    role = Column(String(20), default="student")  # 'student', 'educator', 'admin'
    cluster_label = Column(String(30), default="Steady")  # 'Fast', 'Steady', 'Needs Support'
    streak_days = Column(Integer, default=1)
    xp = Column(Integer, default=150)
    consent_given = Column(Boolean, default=True)
    preferred_lang = Column(String(10), default="en")  # 'en', 'ta', 'hi'
    low_bandwidth_mode = Column(Boolean, default=False)
    high_contrast_mode = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    mastery_records = relationship("MasteryRecord", back_populates="user", cascade="all, delete-orphan")
    interactions = relationship("InteractionLog", back_populates="user", cascade="all, delete-orphan")
    credentials = relationship("Credential", back_populates="user", cascade="all, delete-orphan")
    alerts = relationship("RiskAlert", back_populates="student", cascade="all, delete-orphan")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(50), nullable=False)  # 'Algebra', 'Physics', 'Coding'
    icon = Column(String(50), default="book")

    topics = relationship("Topic", back_populates="course", cascade="all, delete-orphan")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(150), nullable=False)
    slug = Column(String(100), index=True)
    description = Column(Text, nullable=True)
    order_num = Column(Integer, default=1)
    # Store list of prerequisite topic IDs as JSON, e.g. [1, 2]
    prerequisites = Column(JSON, default=list)
    summary_notes = Column(Text, nullable=True)
    formula_sheet = Column(Text, nullable=True)
    simulation_url = Column(String(255), nullable=True)

    course = relationship("Course", back_populates="topics")
    questions = relationship("Question", back_populates="topic", cascade="all, delete-orphan")
    mastery_records = relationship("MasteryRecord", back_populates="topic", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    difficulty = Column(Integer, default=2)  # 1 (Easy) to 5 (Advanced)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # List of 4 strings
    correct_index = Column(Integer, nullable=False)  # 0, 1, 2, or 3
    hint_1 = Column(Text, nullable=True)  # Conceptual nudge
    hint_2 = Column(Text, nullable=True)  # Deeper clue / formula reminder
    step_by_step = Column(Text, nullable=True)  # Guided walkthrough
    explanation = Column(Text, nullable=True)  # Full explanation
    citation_source = Column(String(200), nullable=True)  # E.g., 'Growth Grid STEM Manual, Sec 3.2'

    topic = relationship("Topic", back_populates="questions")


class MasteryRecord(Base):
    __tablename__ = "mastery_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    p_known = Column(Float, default=0.1)  # Bayesian Knowledge Tracing P(L)
    p_transit = Column(Float, default=0.2)  # P(T) - Learning rate
    p_guess = Column(Float, default=0.25)  # P(G) - Guess probability
    p_slip = Column(Float, default=0.10)  # P(S) - Slip probability
    attempts_count = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    is_mastered = Column(Boolean, default=False)  # True when p_known >= 0.80
    last_updated = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="mastery_records")
    topic = relationship("Topic", back_populates="mastery_records")


class InteractionLog(Base):
    __tablename__ = "interaction_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    selected_index = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    response_time_sec = Column(Float, default=15.0)
    hints_used_count = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="interactions")


class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    badge_name = Column(String(150), nullable=False)
    badge_hash = Column(String(66), unique=True, index=True, nullable=False)  # SHA-256 hash (0x...)
    student_hash = Column(String(66), nullable=False)  # Anonymous hash of student ID
    tx_hash = Column(String(66), nullable=True)  # Polygon transaction hash
    network = Column(String(50), default="Polygon Amoy Testnet")
    token_id = Column(Integer, default=1)
    ipfs_metadata_uri = Column(String(255), nullable=True)
    minted_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="credentials")


class RiskAlert(Base):
    __tablename__ = "risk_alerts"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    risk_type = Column(String(50), nullable=False)  # 'Low Mastery', 'Inactivity', 'Repeated Errors'
    severity = Column(String(20), default="medium")  # 'low', 'medium', 'high'
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_resolved = Column(Boolean, default=False)

    student = relationship("User", back_populates="alerts")


class RecommendationFeedback(Base):
    __tablename__ = "recommendation_feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    recommended_topic_id = Column(Integer, nullable=False)
    intervention_type = Column(String(50), default="next_topic")  # 'next_topic', 'remediation', 'review'
    was_helpful = Column(Boolean, default=True)
    score_delta = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
