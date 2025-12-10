from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False, index=True)
    status = Column(String, nullable=False, default="not_started")  # not_started, in_progress, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Ensure one progress record per student-material pair
    __table_args__ = (UniqueConstraint('student_id', 'material_id', name='unique_student_material_progress'),)
    
    def __repr__(self):
        return f"<Progress(student_id={self.student_id}, material_id={self.material_id}, status={self.status})>"
