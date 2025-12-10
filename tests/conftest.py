import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database import Base
from backend.main import app
from backend.models import Student, Material, MaterialProgress, Bookmark
from backend.services.session import _sessions


@pytest.fixture(scope="function")
def db_session():
    """Create a temporary database for testing."""
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    # Create engine with temporary database
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    
    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    
    yield session
    
    # Cleanup
    session.close()
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client for the Flask app."""
    # Override the database session in the app
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client
    
    # Clear sessions after each test
    _sessions.clear()


@pytest.fixture
def sample_student(db_session):
    """Create a sample student for testing."""
    from backend.services.auth import hash_password
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
def authenticated_client(client, sample_student):
    """Create an authenticated test client."""
    from backend.services.session import create_session
    
    # Login the student
    token = create_session(sample_student.id)
    
    # Set cookie in client
    client.set_cookie('localhost', 'session_token', token)
    
    return client
