import pytest
import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base, SessionLocal
from backend.main import app as flask_app

# Store original SessionLocal
_original_session_local = None

@pytest.fixture(scope="function")
def db_session():
    """Create a temporary database for each test."""
    # Create temporary database
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)
    
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Override SessionLocal for this test
    global _original_session_local
    _original_session_local = SessionLocal
    import backend.database
    backend.database.SessionLocal = TestSessionLocal
    
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        os.unlink(db_path)
        # Restore original SessionLocal
        if _original_session_local:
            backend.database.SessionLocal = _original_session_local

@pytest.fixture
def client(db_session):
    """Create a test client with a temporary database."""
    flask_app.config['TESTING'] = True
    flask_app.config['SECRET_KEY'] = 'test-secret-key'
    
    with flask_app.test_client() as client:
        yield client

@pytest.fixture
def sample_student_data():
    """Sample student data for testing."""
    return {
        "email": "test@example.com",
        "name": "Test User",
        "password": "testpassword123"
    }
