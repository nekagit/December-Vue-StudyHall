import pytest
from backend.services.auth import (
    hash_password,
    verify_password,
    authenticate_student,
    create_student,
    get_student_by_email
)

def test_hash_password():
    """Test password hashing."""
    password = "testpassword123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    assert hash1 == hash2
    assert len(hash1) == 64  # SHA256 produces 64 char hex string
    assert hash1 != password

def test_verify_password():
    """Test password verification."""
    password = "testpassword123"
    password_hash = hash_password(password)
    
    assert verify_password(password, password_hash) is True
    assert verify_password("wrongpassword", password_hash) is False

def test_authenticate_student_success(db_session, sample_student_data):
    """Test successful student authentication."""
    # Create a student first
    student = create_student(
        db_session,
        sample_student_data["email"],
        sample_student_data["name"],
        sample_student_data["password"]
    )
    
    # Authenticate
    authenticated = authenticate_student(
        db_session,
        sample_student_data["email"],
        sample_student_data["password"]
    )
    
    assert authenticated is not None
    assert authenticated.id == student.id
    assert authenticated.email == sample_student_data["email"]

def test_authenticate_student_failure(db_session, sample_student_data):
    """Test failed student authentication."""
    # Create a student
    create_student(
        db_session,
        sample_student_data["email"],
        sample_student_data["name"],
        sample_student_data["password"]
    )
    
    # Try wrong password
    authenticated = authenticate_student(
        db_session,
        sample_student_data["email"],
        "wrongpassword"
    )
    assert authenticated is None
    
    # Try wrong email
    authenticated = authenticate_student(
        db_session,
        "wrong@example.com",
        sample_student_data["password"]
    )
    assert authenticated is None

def test_create_student(db_session, sample_student_data):
    """Test student creation."""
    student = create_student(
        db_session,
        sample_student_data["email"],
        sample_student_data["name"],
        sample_student_data["password"]
    )
    
    assert student.id is not None
    assert student.email == sample_student_data["email"]
    assert student.name == sample_student_data["name"]
    assert student.password_hash != sample_student_data["password"]

def test_create_student_duplicate_email(db_session, sample_student_data):
    """Test that duplicate email raises ValueError."""
    create_student(
        db_session,
        sample_student_data["email"],
        sample_student_data["name"],
        sample_student_data["password"]
    )
    
    with pytest.raises(ValueError, match="Email already registered"):
        create_student(
            db_session,
            sample_student_data["email"],
            "Another Name",
            "anotherpassword"
        )

def test_create_student_limit(db_session, sample_student_data):
    """Test 30 student limit."""
    # Create 30 students
    for i in range(30):
        create_student(
            db_session,
            f"test{i}@example.com",
            f"Test User {i}",
            "password123"
        )
    
    # Try to create 31st student
    with pytest.raises(ValueError, match="Maximum of 30 students reached"):
        create_student(
            db_session,
            "test31@example.com",
            "Test User 31",
            "password123"
        )

def test_get_student_by_email(db_session, sample_student_data):
    """Test getting student by email."""
    student = create_student(
        db_session,
        sample_student_data["email"],
        sample_student_data["name"],
        sample_student_data["password"]
    )
    
    found = get_student_by_email(db_session, sample_student_data["email"])
    assert found is not None
    assert found.id == student.id
    
    not_found = get_student_by_email(db_session, "nonexistent@example.com")
    assert not_found is None
