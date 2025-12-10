import pytest
import os
import tempfile
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, SessionLocal
from backend.models import Student, Material, Bookmark, Progress
from backend.services.auth import create_student
from backend.services.session import _sessions
from backend.main import app


@pytest.fixture(autouse=True)
def clear_sessions():
    """Clear sessions before each test for isolation."""
    _sessions.clear()
    yield
    _sessions.clear()


@pytest.fixture(scope="function")
def db_session():
    """Create a temporary database for testing."""
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    # Create engine and session
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
        os.close(db_fd)
        os.unlink(db_path)


@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client for Flask app."""
    # Create test client
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    # Create a callable mock that returns our test session
    class MockSessionLocal:
        def __call__(self):
            return db_session
    
    # Patch SessionLocal in main.py to use our test session
    with patch('backend.main.SessionLocal', MockSessionLocal()):
        with app.test_client() as client:
            yield client


@pytest.fixture
def sample_student(db_session):
    """Create a sample student for testing."""
    student = create_student(
        db_session,
        email="test@example.com",
        name="Test Student",
        password="testpassword123"
    )
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
def authenticated_client(test_client, db_session, sample_student):
    """Create an authenticated test client."""
    # Login to get session token
    response = test_client.post(
        '/api/auth/login',
        json={
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
    )
    
    # Extract session token from cookie
    cookies = response.headers.getlist('Set-Cookie')
    session_token = None
    for cookie in cookies:
        if 'session_token' in cookie:
            session_token = cookie.split('session_token=')[1].split(';')[0]
    
    # Set cookie for subsequent requests
    test_client.set_cookie('localhost', 'session_token', session_token)
    
    return test_client, session_token
