#!/usr/bin/env python3
"""Initialize database with sample data."""
from backend.database import SessionLocal, engine, Base
from backend.models import Student, Material
from backend.services.auth import hash_password

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Demo accounts to create
    demo_accounts = [
        {"email": "student@studyhall.com", "name": "Sample Student", "password": "password123"},
        {"email": "alice@studyhall.com", "name": "Alice Johnson", "password": "demo123"},
        {"email": "bob@studyhall.com", "name": "Bob Smith", "password": "demo123"},
        {"email": "charlie@studyhall.com", "name": "Charlie Brown", "password": "demo123"},
        {"email": "diana@studyhall.com", "name": "Diana Prince", "password": "demo123"},
        {"email": "eve@studyhall.com", "name": "Eve Williams", "password": "demo123"},
    ]
    
    # Create demo accounts (skip if they already exist)
    created_count = 0
    for account in demo_accounts:
        existing = db.query(Student).filter(Student.email == account["email"]).first()
        if not existing:
            student = Student(
                email=account["email"],
                name=account["name"],
                password_hash=hash_password(account["password"])
            )
            db.add(student)
            created_count += 1
            print(f"Created demo account: {account['email']} / {account['password']}")
        else:
            print(f"Account already exists: {account['email']}")
    
    if created_count > 0:
        print(f"\nCreated {created_count} new demo account(s)")
    else:
        print("\nAll demo accounts already exist")
    
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


