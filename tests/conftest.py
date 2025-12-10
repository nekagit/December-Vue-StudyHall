import pytest
import os
import tempfile
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base, SessionLocal
from backend.main import app
from backend.models import Student, Material, Bookmark, Progress
from backend.services.auth import hash_password

# Create a temporary database for testing
@pytest.fixture(scope="function")
def db_session():
    """Create a temporary database session for each test."""
    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def mock_db_session(db_session):
    """Mock SessionLocal to use test database."""
    # SessionLocal is a sessionmaker (callable), so we need to make it return our test session when called
    from unittest.mock import MagicMock
    mock_sessionmaker = MagicMock(return_value=db_session)
    with patch('backend.main.SessionLocal', mock_sessionmaker):
        yield db_session

@pytest.fixture(scope="function")
def test_client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key"
    
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_student(db_session):
    """Create a sample student for testing."""
    student = Student(
        email="test@example.com",
        name="Test User",
        password_hash=hash_password("testpassword123")
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    return student

@pytest.fixture
def sample_material(db_session):
    """Create a sample material for testing."""
    material = Material(
        title="Test Material",
        content="This is test content",
        category="Python",
        order_index=1
    )
    db_session.add(material)
    db_session.commit()
    db_session.refresh(material)
    return material

@pytest.fixture
def authenticated_client(test_client, db_session):
    """Create an authenticated test client."""
    # Create a test student
    student = Student(
        email="auth@example.com",
        name="Auth User",
        password_hash=hash_password("password123")
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    
    # Login to get session token
    response = test_client.post(
        "/api/auth/login",
        json={"email": "auth@example.com", "password": "password123"}
    )
    
    # Return client with session cookie set
    return test_client

@pytest.fixture
def multiple_students(db_session):
    """Create multiple students for testing."""
    students = []
    for i in range(5):
        student = Student(
            email=f"student{i}@example.com",
            name=f"Student {i}",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        students.append(student)
    db_session.commit()
    for student in students:
        db_session.refresh(student)
    return students

@pytest.fixture
def multiple_materials(db_session):
    """Create multiple materials for testing."""
    materials = []
    categories = ["Python", "JavaScript", "Web Dev"]
    for i in range(10):
        material = Material(
            title=f"Material {i}",
            content=f"Content for material {i}",
            category=categories[i % len(categories)],
            order_index=i
        )
        db_session.add(material)
        materials.append(material)
    db_session.commit()
    for material in materials:
        db_session.refresh(material)
    return materials
