"""
SQLAlchemy ORM Models for Career Command Center
All tables with strict data integrity rules
"""
from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Float, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date, datetime

Base = declarative_base()


class UserProfile(Base):
    __tablename__ = "user_profile"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    placement_status = Column(String, default="pending")  # "pending" | "secured" | "failed_Feb2027"
    group_c_status = Column(String, default="pending")  # "pending" | "prelim_cleared" | "not_cleared"
    current_phase = Column(Integer, default=1)  # Phases: 1, 2, 3, 4, 5
    start_date = Column(Date, default=date(2026, 6, 26))
    last_updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    counts_for = Column(JSON, nullable=False)  # ["placement", "ssc", "mpsc_group_c", "mpsc_group_b"]
    phase_introduced = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    
    topics = relationship("Topic", back_populates="subject")


class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    name = Column(String, nullable=False)
    part_number = Column(Integer, nullable=True)
    total_parts = Column(Integer, nullable=True)
    subtopics = Column(JSON, nullable=False)  # List of exact subtopics
    sequence_order = Column(Integer, nullable=False)
    phase = Column(Integer, nullable=False)
    scheduled_date = Column(Date, nullable=True)
    
    subject = relationship("Subject", back_populates="topics")
    checklist_items = relationship("ChecklistItem", back_populates="topic")


class ChecklistItem(Base):
    __tablename__ = "checklist_items"
    
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    item_type = Column(String, nullable=False)  # "learn" | "notes" | "practice" | "revise_d3" | "revise_d7" | "revise_d10" | "current_affairs" | "mock"
    description = Column(String, nullable=False)
    scheduled_date = Column(Date, nullable=False)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)  # Write-once, never overwrite
    time_spent_minutes = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    skipped = Column(Boolean, default=False)
    skip_reason = Column(String, nullable=True)
    
    topic = relationship("Topic", back_populates="checklist_items")


class RevisionSchedule(Base):
    __tablename__ = "revision_schedule"
    
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    learn_completed_date = Column(Date, nullable=False)
    revision_d3_date = Column(Date, nullable=False)
    revision_d7_date = Column(Date, nullable=False)
    revision_d10_date = Column(Date, nullable=False)
    revision_d3_done = Column(Boolean, default=False)
    revision_d7_done = Column(Boolean, default=False)
    revision_d10_done = Column(Boolean, default=False)


class TopicMastery(Base):
    __tablename__ = "topic_mastery"
    
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, unique=True)
    learn_done = Column(Boolean, default=False)
    notes_done = Column(Boolean, default=False)
    practice_done = Column(Boolean, default=False)
    revise_d3_done = Column(Boolean, default=False)
    revise_d7_done = Column(Boolean, default=False)
    revise_d10_done = Column(Boolean, default=False)
    mastered = Column(Boolean, default=False)


class Note(Base):
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    pinned = Column(Boolean, default=False)
    archived = Column(Boolean, default=False)


class MockTest(Base):
    __tablename__ = "mock_tests"
    
    id = Column(Integer, primary_key=True)
    exam_type = Column(String, nullable=False)  # "placement_aptitude" | "placement_dsa" | "ssc_tier1" | "ssc_tier2" | "mpsc_group_c" | "mpsc_group_b" | "custom"
    test_name = Column(String, nullable=False)
    taken_on = Column(Date, nullable=False)
    total_questions = Column(Integer, nullable=False)
    attempted = Column(Integer, nullable=False)
    correct = Column(Integer, nullable=False)
    wrong = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    time_taken_minutes = Column(Integer, nullable=False)
    subject_breakdown = Column(JSON, nullable=True)  # {"Subject": {"correct": X, "wrong": Y, "attempted": Z}}
    notes = Column(Text, nullable=True)


class DailyLog(Base):
    __tablename__ = "daily_log"
    
    id = Column(Integer, primary_key=True)
    log_date = Column(Date, unique=True, nullable=False)
    total_study_minutes = Column(Integer, default=0)
    tasks_completed = Column(Integer, default=0)
    tasks_total = Column(Integer, default=0)
    phase = Column(Integer, nullable=False)
    streak_day = Column(Integer, default=0)
