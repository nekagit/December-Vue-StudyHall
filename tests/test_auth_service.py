import pytest
from backend.services.auth import (
    hash_password,
    verify_password,
    authenticate_student,
    create_student,
    get_student_by_email
)
from backend.models import Student


class TestPasswordHashing:
    """Test password hashing functions."""
    
    def test_hash_password(self):
        """Test password hashing produces consistent output."""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 produces 64 character hex string
        assert hash1 != password  # Hash should be different from password
    
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
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        db_session.commit()
        
        authenticated = authenticate_student(db_session, "test@example.com", "password123")
        
        assert authenticated is not None
        assert authenticated.email == "test@example.com"
        assert authenticated.id == student.id
    
    def test_authenticate_student_wrong_password(self, db_session):
        """Test authentication with wrong password."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("correctpassword")
        )
        db_session.add(student)
        db_session.commit()
        
        authenticated = authenticate_student(db_session, "test@example.com", "wrongpassword")
        
        assert authenticated is None
    
    def test_authenticate_student_nonexistent_email(self, db_session):
        """Test authentication with non-existent email."""
        authenticated = authenticate_student(db_session, "nonexistent@example.com", "password123")
        
        assert authenticated is None


class TestCreateStudent:
    """Test student creation."""
    
    def test_create_student_success(self, db_session):
        """Test successful student creation."""
        student = create_student(
            db_session,
            email="newuser@example.com",
            name="New User",
            password="password123"
        )
        
        assert student is not None
        assert student.email == "newuser@example.com"
        assert student.name == "New User"
        assert student.password_hash != "password123"  # Should be hashed
        assert verify_password("password123", student.password_hash) is True
        
        # Verify student was saved to database
        saved_student = db_session.query(Student).filter(Student.email == "newuser@example.com").first()
        assert saved_student is not None
        assert saved_student.id == student.id
    
    def test_create_student_duplicate_email(self, db_session):
        """Test creating student with duplicate email."""
        create_student(
            db_session,
            email="test@example.com",
            name="First User",
            password="password123"
        )
        
        with pytest.raises(ValueError, match="Email already registered"):
            create_student(
                db_session,
                email="test@example.com",
                name="Second User",
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
        
        # Try to create one more
        with pytest.raises(ValueError, match="Maximum of 30 students reached"):
            create_student(
                db_session,
                email="newstudent@example.com",
                name="New Student",
                password="password123"
            )


class TestGetStudentByEmail:
    """Test getting student by email."""
    
    def test_get_student_by_email_exists(self, db_session):
        """Test getting existing student by email."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        db_session.commit()
        
        found = get_student_by_email(db_session, "test@example.com")
        
        assert found is not None
        assert found.email == "test@example.com"
        assert found.id == student.id
    
    def test_get_student_by_email_not_exists(self, db_session):
        """Test getting non-existent student by email."""
        found = get_student_by_email(db_session, "nonexistent@example.com")
        
        assert found is None
