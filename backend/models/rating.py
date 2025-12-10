from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    material_id = Column(Integer, ForeignKey("materials.id"), nullable=False, index=True)
    rating = Column(Float, nullable=False)  # 1.0 to 5.0
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Ensure one rating per student per material
    __table_args__ = (UniqueConstraint('student_id', 'material_id', name='unique_student_material_rating'),)
    
    # Relationships
    student = relationship("Student", backref="ratings")
    material = relationship("Material", backref="ratings")
    
    def __repr__(self):
        return f"<Rating(id={self.id}, student_id={self.student_id}, material_id={self.material_id}, rating={self.rating})>"
