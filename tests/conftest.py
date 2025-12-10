import pytest
import os
import tempfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.main import app

# Create a temporary database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_db_engine():
    """Create a test database engine."""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def api_db_session(test_db_engine):
    """Create a database session for API tests using the same engine as client."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(test_db_engine):
    """Create a test client for the Flask app with test database."""
    # Create a test sessionmaker
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
    
    # Patch SessionLocal in both backend.database and backend.main to use test database
    from unittest.mock import patch
    import backend.database
    import backend.main
    
    original_session_local_db = backend.database.SessionLocal
    original_session_local_main = backend.main.SessionLocal
    
    # Replace SessionLocal with test version
    backend.database.SessionLocal = TestingSessionLocal
    backend.main.SessionLocal = TestingSessionLocal
    
    try:
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret-key"
        with app.test_client() as client:
            yield client
    finally:
        # Restore original SessionLocal
        backend.database.SessionLocal = original_session_local_db
        backend.main.SessionLocal = original_session_local_main

@pytest.fixture
def sample_student_data():
    """Sample student data for testing."""
    return {
        "email": "test@example.com",
        "name": "Test Student",
        "password": "testpassword123"
    }

@pytest.fixture
def sample_material_data():
    """Sample material data for testing."""
    return {
        "title": "Test Material",
        "content": "This is test content",
        "category": "Python",
        "notion_url": "https://notion.so/test",
        "notion_page_id": "test-page-id-123"
    }
