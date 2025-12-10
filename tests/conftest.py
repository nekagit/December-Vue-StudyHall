import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.models import Student, Material, Bookmark, Progress, Note, Rating, StudySession, StudyStreak
from backend.services.auth import hash_password
from unittest.mock import patch
from backend.main import app as flask_app


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_sql_app.db"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_patch():
    """Patch SessionLocal to use test database."""
    with patch('backend.main.SessionLocal', TestingSessionLocal):
        yield


@pytest.fixture
def client(db_patch):
    """Create a test client for Flask app."""
    flask_app.config['TESTING'] = True
    flask_app.config['SECRET_KEY'] = 'test-secret-key'
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def sample_student(db):
    """Create a sample student for testing."""
    student = Student(
        email="test@example.com",
        name="Test User",
        password_hash=hash_password("testpassword123")
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@pytest.fixture
def sample_material(db):
    """Create a sample material for testing."""
    material = Material(
        title="Test Material",
        content="This is test content",
        category="Python",
        order_index=1
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


@pytest.fixture
def authenticated_client(client, db, sample_student):
    """Create an authenticated test client."""
    from backend.services.session import create_session
    
    token = create_session(sample_student.id)
    client.set_cookie('localhost', 'session_token', token)
    return client
