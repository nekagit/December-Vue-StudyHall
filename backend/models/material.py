from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from backend.database import Base

class Material(Base):
    __tablename__ = "materials"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    content = Column(Text)  # Markdown or HTML content
    notion_page_id = Column(String, unique=True, index=True)  # Notion page ID if synced
    notion_url = Column(String)  # Original Notion URL
    category = Column(String)  # e.g., "Python", "Web Dev", etc.
    order_index = Column(Integer, default=0)  # For ordering materials
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Material(id={self.id}, title={self.title[:50]})>"











