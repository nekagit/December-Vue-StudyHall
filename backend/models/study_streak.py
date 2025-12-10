from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class StudyStreak(Base):
    __tablename__ = "study_streaks"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, unique=True, index=True)
    current_streak = Column(Integer, default=0)  # Current consecutive days
    longest_streak = Column(Integer, default=0)  # Longest streak achieved
    last_study_date = Column(DateTime(timezone=True))  # Last date with study activity
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<StudyStreak(id={self.id}, student_id={self.student_id}, current_streak={self.current_streak})>"
