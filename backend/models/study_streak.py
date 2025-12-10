from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class StudyStreak(Base):
    __tablename__ = "study_streaks"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, unique=True, index=True)  # One streak per student
    current_streak_days = Column(Integer, default=0)  # Current consecutive days
    longest_streak_days = Column(Integer, default=0)  # Best streak ever
    last_study_date = Column(DateTime(timezone=True), nullable=True)  # Last date student studied
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", backref="study_streak", uselist=False)
    
    def __repr__(self):
        return f"<StudyStreak(id={self.id}, student_id={self.student_id}, current={self.current_streak_days}days)>"
