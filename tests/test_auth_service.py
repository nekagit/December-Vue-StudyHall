import pytest
from backend.services.auth import (
    hash_password,
    verify_password,
    authenticate_student,
    get_student_by_email,
    create_student
)
from backend.models.student import Student


class TestPasswordHashing:
    """Tests for password hashing functions."""
    
    def test_hash_password(self):
        """Test password hashing produces consistent results."""
        password = "testpassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 produces 64 character hex string
        assert hash1 != password  # Hash should be different from password
    
    def test_hash_password_different_passwords(self):
        """Test that different passwords produce different hashes."""
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
    """Tests for student authentication."""
    
    def test_authenticate_student_success(self, db_session, sample_student_data):
        """Test successful authentication."""
        # Create a student
        student = Student(
            email=sample_student_data["email"],
            name=sample_student_data["name"],
            password_hash=hash_password(sample_student_data["password"])
        )
        db_session.add(student)
        db_session.commit()
        
        # Authenticate
        authenticated = authenticate_student(
            db_session,
            sample_student_data["email"],
            sample_student_data["password"]
        )
        
        assert authenticated is not None
        assert authenticated.id == student.id
        assert authenticated.email == sample_student_data["email"]
    
    def test_authenticate_student_wrong_password(self, db_session, sample_student_data):
        """Test authentication with wrong password."""
        student = Student(
            email=sample_student_data["email"],
            name=sample_student_data["name"],
            password_hash=hash_password(sample_student_data["password"])
        )
        db_session.add(student)
        db_session.commit()
        
        authenticated = authenticate_student(
            db_session,
            sample_student_data["email"],
            "wrongpassword"
        )
        
        assert authenticated is None
    
    def test_authenticate_student_nonexistent_email(self, db_session):
        """Test authentication with non-existent email."""
        authenticated = authenticate_student(
            db_session,
            "nonexistent@example.com",
            "password"
        )
        
        assert authenticated is None


class TestGetStudentByEmail:
    """Tests for getting student by email."""
    
    def test_get_student_by_email_exists(self, db_session, sample_student_data):
        """Test getting existing student by email."""
        student = Student(
            email=sample_student_data["email"],
            name=sample_student_data["name"],
            password_hash="hash"
        )
        db_session.add(student)
        db_session.commit()
        
        found = get_student_by_email(db_session, sample_student_data["email"])
        
        assert found is not None
        assert found.id == student.id
        assert found.email == sample_student_data["email"]
    
    def test_get_student_by_email_not_exists(self, db_session):
        """Test getting non-existent student by email."""
        found = get_student_by_email(db_session, "nonexistent@example.com")
        
        assert found is None


class TestCreateStudent:
    """Tests for creating a new student."""
    
    def test_create_student_success(self, db_session, sample_student_data):
        """Test successful student creation."""
        student = create_student(
            db_session,
            sample_student_data["email"],
            sample_student_data["name"],
            sample_student_data["password"]
        )
        
        assert student.id is not None
        assert student.email == sample_student_data["email"]
        assert student.name == sample_student_data["name"]
        assert student.password_hash == hash_password(sample_student_data["password"])
        
        # Verify it's in the database
        found = db_session.query(Student).filter(Student.id == student.id).first()
        assert found is not None
        assert found.email == sample_student_data["email"]
    
    def test_create_student_duplicate_email(self, db_session, sample_student_data):
        """Test creating student with duplicate email."""
        create_student(
            db_session,
            sample_student_data["email"],
            sample_student_data["name"],
            sample_student_data["password"]
        )
        
        # Try to create another student with same email
        with pytest.raises(ValueError, match="Email already registered"):
            create_student(
                db_session,
                sample_student_data["email"],
                "Another Name",
                "anotherpassword"
            )
    
    def test_create_student_max_limit(self, db_session):
        """Test that student creation fails at 30 student limit."""
        # Create 30 students
        for i in range(30):
            create_student(
                db_session,
                f"student{i}@example.com",
                f"Student {i}",
                "password"
            )
        
        # Try to create 31st student
        with pytest.raises(ValueError, match="Maximum of 30 students reached"):
            create_student(
                db_session,
                "student31@example.com",
                "Student 31",
                "password"
            )
