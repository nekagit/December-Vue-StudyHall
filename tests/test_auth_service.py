import pytest
from backend.services.auth import (
    hash_password,
    verify_password,
    authenticate_student,
    get_student_by_email,
    create_student
)
from backend.models import Student


class TestPasswordHashing:
    """Test password hashing functions."""
    
    def test_hash_password(self):
        """Test password hashing produces consistent results."""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 == hash2
        assert isinstance(hash1, str)
        assert len(hash1) == 64  # SHA256 produces 64 character hex string
    
    def test_hash_password_different_passwords(self):
        """Test different passwords produce different hashes."""
        hash1 = hash_password("password1")
        hash2 = hash_password("password2")
        
        assert hash1 != hash2
    
    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        password = "testpassword123"
        password_hash = hash_password(password)
        
        assert verify_password(password, password_hash) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        password_hash = hash_password(password)
        
        assert verify_password(wrong_password, password_hash) is False


class TestAuthenticateStudent:
    """Test student authentication."""
    
    def test_authenticate_student_success(self, db_session):
        """Test successful authentication."""
        student = create_student(
            db_session,
            email="test@example.com",
            name="Test Student",
            password="password123"
        )
        
        authenticated = authenticate_student(
            db_session,
            "test@example.com",
            "password123"
        )
        
        assert authenticated is not None
        assert authenticated.id == student.id
        assert authenticated.email == student.email
    
    def test_authenticate_student_wrong_email(self, db_session):
        """Test authentication with wrong email."""
        create_student(
            db_session,
            email="test@example.com",
            name="Test Student",
            password="password123"
        )
        
        authenticated = authenticate_student(
            db_session,
            "wrong@example.com",
            "password123"
        )
        
        assert authenticated is None
    
    def test_authenticate_student_wrong_password(self, db_session):
        """Test authentication with wrong password."""
        create_student(
            db_session,
            email="test@example.com",
            name="Test Student",
            password="password123"
        )
        
        authenticated = authenticate_student(
            db_session,
            "test@example.com",
            "wrongpassword"
        )
        
        assert authenticated is None
    
    def test_authenticate_student_nonexistent(self, db_session):
        """Test authentication with non-existent student."""
        authenticated = authenticate_student(
            db_session,
            "nonexistent@example.com",
            "password123"
        )
        
        assert authenticated is None


class TestGetStudentByEmail:
    """Test getting student by email."""
    
    def test_get_student_by_email_exists(self, db_session):
        """Test getting existing student by email."""
        student = create_student(
            db_session,
            email="test@example.com",
            name="Test Student",
            password="password123"
        )
        
        found = get_student_by_email(db_session, "test@example.com")
        
        assert found is not None
        assert found.id == student.id
        assert found.email == student.email
    
    def test_get_student_by_email_not_exists(self, db_session):
        """Test getting non-existent student by email."""
        found = get_student_by_email(db_session, "nonexistent@example.com")
        
        assert found is None


class TestCreateStudent:
    """Test student creation."""
    
    def test_create_student_success(self, db_session):
        """Test successful student creation."""
        student = create_student(
            db_session,
            email="newstudent@example.com",
            name="New Student",
            password="password123"
        )
        
        assert student.id is not None
        assert student.email == "newstudent@example.com"
        assert student.name == "New Student"
        assert student.password_hash is not None
        assert student.is_active is True
    
    def test_create_student_duplicate_email(self, db_session):
        """Test creating student with duplicate email."""
        create_student(
            db_session,
            email="test@example.com",
            name="First Student",
            password="password123"
        )
        
        with pytest.raises(ValueError, match="already registered"):
            create_student(
                db_session,
                email="test@example.com",
                name="Second Student",
                password="password123"
            )
    
    def test_create_student_max_limit(self, db_session):
        """Test creating student when max limit is reached."""
        # Create 30 students
        for i in range(30):
            create_student(
                db_session,
                email=f"student{i}@example.com",
                name=f"Student {i}",
                password="password123"
            )
        
        # Try to create 31st student
        with pytest.raises(ValueError, match="30"):
            create_student(
                db_session,
                email="student31@example.com",
                name="Student 31",
                password="password123"
            )
    
    def test_create_student_password_hash(self, db_session):
        """Test that password is properly hashed."""
        student = create_student(
            db_session,
            email="test@example.com",
            name="Test Student",
            password="password123"
        )
        
        # Password hash should not be plain text
        assert student.password_hash != "password123"
        assert len(student.password_hash) == 64  # SHA256 hash length
        
        # Should be able to verify password
        assert verify_password("password123", student.password_hash) is True
    
    def test_create_student_case_sensitive_email(self, db_session):
        """Test that email is case-sensitive for uniqueness."""
        create_student(
            db_session,
            email="Test@Example.com",
            name="First Student",
            password="password123"
        )
        
        # SQLite is case-insensitive by default, but we should still test
        # In production with PostgreSQL, this would be case-sensitive
        # For now, we'll test that lowercase version works
        student2 = create_student(
            db_session,
            email="test@example.com",
            name="Second Student",
            password="password123"
        )
        
        # Depending on database configuration, this might fail or succeed
        # For SQLite, it will likely succeed as a different email
        assert student2 is not None
