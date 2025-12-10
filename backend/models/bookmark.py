from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Ensure a student can only bookmark a material once
    __table_args__ = (UniqueConstraint('student_id', 'material_id', name='unique_student_material_bookmark'),)
    
    def __repr__(self):
        return f"<Bookmark(student_id={self.student_id}, material_id={self.material_id})>"
