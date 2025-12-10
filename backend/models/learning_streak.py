from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class LearningStreak(Base):
    __tablename__ = "learning_streaks"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, unique=True, index=True)
    current_streak_days = Column(Integer, default=0)  # Current consecutive days
    longest_streak_days = Column(Integer, default=0)  # Longest streak ever achieved
    last_study_date = Column(DateTime(timezone=True), nullable=True)  # Last date student studied
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", backref="learning_streak", uselist=False)
    
    def __repr__(self):
        return f"<LearningStreak(id={self.id}, student_id={self.student_id}, current={self.current_streak_days}days)>"
