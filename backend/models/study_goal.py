from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class StudyGoal(Base):
    __tablename__ = "study_goals"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    target_date = Column(DateTime(timezone=True), nullable=True)  # Optional deadline
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=True, index=True)  # Optional - link to specific material
    target_minutes = Column(Integer, nullable=True)  # Optional - target study time in minutes
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", backref="study_goals")
    material = relationship("Material", backref="study_goals")
    
    def __repr__(self):
        return f"<StudyGoal(id={self.id}, student_id={self.student_id}, title={self.title[:50]})>"
