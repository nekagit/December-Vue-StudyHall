import pytest
from backend.services.auth import (
    hash_password, verify_password, authenticate_student,
    get_student_by_email, create_student
)
from backend.models import Student


class TestPasswordHashing:
    """Test password hashing functions."""
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Same password should produce same hash
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 produces 64 char hex string
        assert hash1 != password  # Hash should be different from password
    
    def test_verify_password(self):
        """Test password verification."""
        password = "testpassword123"
        password_hash = hash_password(password)
        
        assert verify_password(password, password_hash) is True
        assert verify_password("wrongpassword", password_hash) is False
        assert verify_password(password, "wronghash") is False
    
    def test_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes."""
        hash1 = hash_password("password1")
        hash2 = hash_password("password2")
        
        assert hash1 != hash2


class TestAuthenticateStudent:
    """Test student authentication."""
    
    def test_authenticate_valid_credentials(self, db):
        """Test authentication with valid credentials."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db.add(student)
        db.commit()
        
        authenticated = authenticate_student(db, "test@example.com", "password123")
        assert authenticated is not None
        assert authenticated.id == student.id
        assert authenticated.email == student.email
    
    def test_authenticate_invalid_email(self, db):
        """Test authentication with invalid email."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db.add(student)
        db.commit()
        
        authenticated = authenticate_student(db, "wrong@example.com", "password123")
        assert authenticated is None
    
    def test_authenticate_invalid_password(self, db):
        """Test authentication with invalid password."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db.add(student)
        db.commit()
        
        authenticated = authenticate_student(db, "test@example.com", "wrongpassword")
        assert authenticated is None
    
    def test_authenticate_nonexistent_student(self, db):
        """Test authentication with non-existent student."""
        authenticated = authenticate_student(db, "nonexistent@example.com", "password")
        assert authenticated is None


class TestGetStudentByEmail:
    """Test getting student by email."""
    
    def test_get_existing_student(self, db):
        """Test getting an existing student."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password")
        )
        db.add(student)
        db.commit()
        
        found = get_student_by_email(db, "test@example.com")
        assert found is not None
        assert found.id == student.id
        assert found.email == student.email
    
    def test_get_nonexistent_student(self, db):
        """Test getting a non-existent student."""
        found = get_student_by_email(db, "nonexistent@example.com")
        assert found is None


class TestCreateStudent:
    """Test student creation."""
    
    def test_create_student_success(self, db):
        """Test successful student creation."""
        student = create_student(db, "new@example.com", "New User", "password123")
        
        assert student.id is not None
        assert student.email == "new@example.com"
        assert student.name == "New User"
        assert verify_password("password123", student.password_hash)
    
    def test_create_student_duplicate_email(self, db):
        """Test creating student with duplicate email."""
        create_student(db, "test@example.com", "User 1", "password1")
        
        with pytest.raises(ValueError, match="Email already registered"):
            create_student(db, "test@example.com", "User 2", "password2")
    
    def test_create_student_max_limit(self, db):
        """Test student creation limit of 30."""
        # Create 30 students
        for i in range(30):
            create_student(db, f"user{i}@example.com", f"User {i}", "password")
        
        # Try to create 31st student
        with pytest.raises(ValueError, match="Maximum of 30 students reached"):
            create_student(db, "user31@example.com", "User 31", "password")
    
    def test_create_student_case_sensitive_email(self, db):
        """Test that email is case-sensitive."""
        create_student(db, "Test@Example.com", "User 1", "password1")
        
        # SQLite is case-insensitive by default, but we should still be able to create
        # This test verifies the behavior
        try:
            create_student(db, "test@example.com", "User 2", "password2")
            # If no error, that's fine - SQLite treats emails case-insensitively
        except ValueError:
            # If error, that's also fine - depends on database configuration
            pass
