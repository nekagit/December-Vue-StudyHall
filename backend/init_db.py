#!/usr/bin/env python3
"""Initialize database with sample data."""
from backend.database import SessionLocal, engine, Base
from backend.models import Material

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Create sample materials
    if db.query(Material).count() == 0:
        materials = [
            Material(
                title="Python Basics",
                content="# Python Basics\n\nWelcome to Python! This is a sample material.",
                category="Python",
                order_index=1
            ),
            Material(
                title="Data Structures",
                content="# Data Structures\n\nLearn about lists, dictionaries, and more.",
                category="Python",
                order_index=2
            ),
            Material(
                title="Web Development Intro",
                content="# Web Development\n\nIntroduction to HTML, CSS, and JavaScript.",
                category="Web Dev",
                order_index=3
            )
        ]
        for material in materials:
            db.add(material)
        print("Created sample materials")
    
    db.commit()
    print("Database initialized successfully!")
except Exception as e:
    db.rollback()
    print(f"Error initializing database: {e}")
finally:
    db.close()


