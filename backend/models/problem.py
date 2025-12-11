from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from backend.database import Base

class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)  # Short description
    full_description = Column(Text)  # Detailed description with examples
    difficulty = Column(String, nullable=False, index=True)  # beginner, intermediate, advanced
    tags = Column(JSON)  # List of tags like ["Basics", "Math", "Lists"]
    points = Column(Integer, default=10)
    estimated_time = Column(Integer)  # Estimated time in minutes
    examples = Column(JSON)  # List of {input: str, output: str}
    constraints = Column(JSON)  # List of constraint strings
    test_cases = Column(JSON, nullable=False)  # List of {input: str, output: str}
    starter_code = Column(Text)  # Optional starter code template
    category = Column(String)  # Optional category grouping
    order_index = Column(Integer, default=0)  # For ordering problems
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Problem(id={self.id}, title={self.title[:50]}, difficulty={self.difficulty})>"

