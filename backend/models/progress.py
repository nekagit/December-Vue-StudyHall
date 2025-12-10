from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False, index=True)
    status = Column(String, default="not_started")  # not_started, in_progress, completed
    progress_percentage = Column(Float, default=0.0)  # 0.0 to 100.0
    last_accessed_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", backref="progress_records")
    material = relationship("Material", backref="progress_records")
    
    def __repr__(self):
        return f"<Progress(id={self.id}, student_id={self.student_id}, material_id={self.material_id}, status={self.status})>"
