from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class MaterialProgress(Base):
    __tablename__ = "material_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False, index=True)
    is_completed = Column(Boolean, default=False)
    progress_percentage = Column(Integer, default=0)  # 0-100
    last_accessed_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<MaterialProgress(student_id={self.student_id}, material_id={self.material_id}, completed={self.is_completed})>"
