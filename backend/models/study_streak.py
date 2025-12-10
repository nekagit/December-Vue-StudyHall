from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class StudyStreak(Base):
    __tablename__ = "study_streaks"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, unique=True, index=True)
    current_streak = Column(Integer, default=0)  # Current consecutive days
    longest_streak = Column(Integer, default=0)  # Longest streak ever
    last_study_date = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", backref="study_streak", uselist=False)
    
    def __repr__(self):
        return f"<StudyStreak(id={self.id}, student_id={self.student_id}, current={self.current_streak}, longest={self.longest_streak})>"
