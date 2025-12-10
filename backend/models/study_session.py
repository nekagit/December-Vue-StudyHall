from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=True, index=True)  # Optional - can be general study
    duration_minutes = Column(Float, nullable=False, default=0.0)  # Duration in minutes
    notes = Column(Text, nullable=True)  # Optional notes about the session
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", backref="study_sessions")
    material = relationship("Material", backref="study_sessions")
    
    def __repr__(self):
        return f"<StudySession(id={self.id}, student_id={self.student_id}, duration={self.duration_minutes}min)>"
