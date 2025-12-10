from typing import Optional
from sqlalchemy.orm import Session
from backend.models.student import Student
import hashlib

def hash_password(password: str) -> str:
    """Simple password hashing for MVP. Use bcrypt in production."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash."""
    return hash_password(password) == password_hash

def authenticate_student(db: Session, email: str, password: str) -> Optional[Student]:
    """Authenticate a student by email and password."""
    student = db.query(Student).filter(Student.email == email).first()
    if student and verify_password(password, student.password_hash):
        return student
    return None

def get_student_by_email(db: Session, email: str) -> Optional[Student]:
    """Get student by email."""
    return db.query(Student).filter(Student.email == email).first()

def create_student(db: Session, email: str, name: str, password: str) -> Student:
    """Create a new student."""
    # Check if we're at the 30 student limit
    student_count = db.query(Student).count()
    if student_count >= 30:
        raise ValueError("Maximum of 30 students reached")
    
    # Check if email already exists
    if get_student_by_email(db, email):
        raise ValueError("Email already registered")
    
    student = Student(
        email=email,
        name=name,
        password_hash=hash_password(password)
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


