import pytest
from datetime import datetime
from backend.models import (
    Student, Material, Bookmark, Progress, Note, Rating, 
    StudySession, StudyStreak
)
from backend.services.auth import hash_password


class TestStudent:
    """Test Student model."""
    
    def test_create_student(self, db):
        """Test creating a student."""
        student = Student(
            email="student@example.com",
            name="John Doe",
            password_hash=hash_password("password123")
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        
        assert student.id is not None
        assert student.email == "student@example.com"
        assert student.name == "John Doe"
        assert student.is_active is True
        assert student.created_at is not None
    
    def test_student_repr(self, db):
        """Test student string representation."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password")
        )
        db.add(student)
        db.commit()
        
        repr_str = repr(student)
        assert "Student" in repr_str
        assert "test@example.com" in repr_str
        assert "Test User" in repr_str


class TestMaterial:
    """Test Material model."""
    
    def test_create_material(self, db):
        """Test creating a material."""
        material = Material(
            title="Python Basics",
            content="Introduction to Python programming",
            category="Python",
            order_index=1,
            notion_page_id="notion-123",
            notion_url="https://notion.so/test"
        )
        db.add(material)
        db.commit()
        db.refresh(material)
        
        assert material.id is not None
        assert material.title == "Python Basics"
        assert material.content == "Introduction to Python programming"
        assert material.category == "Python"
        assert material.order_index == 1
        assert material.notion_page_id == "notion-123"
        assert material.created_at is not None
    
    def test_material_repr(self, db):
        """Test material string representation."""
        material = Material(
            title="A" * 100,  # Long title
            content="Content"
        )
        db.add(material)
        db.commit()
        
        repr_str = repr(material)
        assert "Material" in repr_str
        assert len(repr_str) < 100  # Should truncate long titles


class TestBookmark:
    """Test Bookmark model."""
    
    def test_create_bookmark(self, db, sample_student, sample_material):
        """Test creating a bookmark."""
        bookmark = Bookmark(
            student_id=sample_student.id,
            material_id=sample_material.id
        )
        db.add(bookmark)
        db.commit()
        db.refresh(bookmark)
        
        assert bookmark.id is not None
        assert bookmark.student_id == sample_student.id
        assert bookmark.material_id == sample_material.id
        assert bookmark.created_at is not None
        assert bookmark.student == sample_student
        assert bookmark.material == sample_material
    
    def test_bookmark_repr(self, db, sample_student, sample_material):
        """Test bookmark string representation."""
        bookmark = Bookmark(
            student_id=sample_student.id,
            material_id=sample_material.id
        )
        db.add(bookmark)
        db.commit()
        
        repr_str = repr(bookmark)
        assert "Bookmark" in repr_str
        assert str(sample_student.id) in repr_str
        assert str(sample_material.id) in repr_str


class TestProgress:
    """Test Progress model."""
    
    def test_create_progress(self, db, sample_student, sample_material):
        """Test creating a progress record."""
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id,
            status="in_progress",
            progress_percentage=50.0
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
        
        assert progress.id is not None
        assert progress.student_id == sample_student.id
        assert progress.material_id == sample_material.id
        assert progress.status == "in_progress"
        assert progress.progress_percentage == 50.0
        assert progress.last_accessed_at is not None
        assert progress.created_at is not None
    
    def test_progress_defaults(self, db, sample_student, sample_material):
        """Test progress default values."""
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
        
        assert progress.status == "not_started"
        assert progress.progress_percentage == 0.0
        assert progress.completed_at is None
    
    def test_progress_repr(self, db, sample_student, sample_material):
        """Test progress string representation."""
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id,
            status="completed"
        )
        db.add(progress)
        db.commit()
        
        repr_str = repr(progress)
        assert "Progress" in repr_str
        assert "completed" in repr_str


class TestNote:
    """Test Note model."""
    
    def test_create_note(self, db, sample_student, sample_material):
        """Test creating a note."""
        note = Note(
            student_id=sample_student.id,
            material_id=sample_material.id,
            content="This is a test note"
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        
        assert note.id is not None
        assert note.student_id == sample_student.id
        assert note.material_id == sample_material.id
        assert note.content == "This is a test note"
        assert note.created_at is not None
        assert note.student == sample_student
        assert note.material == sample_material
    
    def test_note_repr(self, db, sample_student, sample_material):
        """Test note string representation."""
        note = Note(
            student_id=sample_student.id,
            material_id=sample_material.id,
            content="Test content"
        )
        db.add(note)
        db.commit()
        
        repr_str = repr(note)
        assert "Note" in repr_str
        assert str(sample_student.id) in repr_str


class TestRating:
    """Test Rating model."""
    
    def test_create_rating(self, db, sample_student, sample_material):
        """Test creating a rating."""
        rating = Rating(
            student_id=sample_student.id,
            material_id=sample_material.id,
            rating=5,
            comment="Great material!"
        )
        db.add(rating)
        db.commit()
        db.refresh(rating)
        
        assert rating.id is not None
        assert rating.student_id == sample_student.id
        assert rating.material_id == sample_material.id
        assert rating.rating == 5
        assert rating.comment == "Great material!"
        assert rating.created_at is not None
        assert rating.student == sample_student
        assert rating.material == sample_material
    
    def test_rating_without_comment(self, db, sample_student, sample_material):
        """Test creating a rating without comment."""
        rating = Rating(
            student_id=sample_student.id,
            material_id=sample_material.id,
            rating=4
        )
        db.add(rating)
        db.commit()
        db.refresh(rating)
        
        assert rating.rating == 4
        assert rating.comment is None
    
    def test_rating_repr(self, db, sample_student, sample_material):
        """Test rating string representation."""
        rating = Rating(
            student_id=sample_student.id,
            material_id=sample_material.id,
            rating=5
        )
        db.add(rating)
        db.commit()
        
        repr_str = repr(rating)
        assert "Rating" in repr_str
        assert "5" in repr_str


class TestStudySession:
    """Test StudySession model."""
    
    def test_create_study_session(self, db, sample_student, sample_material):
        """Test creating a study session."""
        session = StudySession(
            student_id=sample_student.id,
            material_id=sample_material.id,
            duration_minutes=30.5,
            notes="Studied Python basics"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        assert session.id is not None
        assert session.student_id == sample_student.id
        assert session.material_id == sample_material.id
        assert session.duration_minutes == 30.5
        assert session.notes == "Studied Python basics"
        assert session.started_at is not None
        assert session.created_at is not None
    
    def test_study_session_without_material(self, db, sample_student):
        """Test creating a study session without material."""
        session = StudySession(
            student_id=sample_student.id,
            duration_minutes=15.0
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        assert session.material_id is None
        assert session.duration_minutes == 15.0
    
    def test_study_session_repr(self, db, sample_student):
        """Test study session string representation."""
        session = StudySession(
            student_id=sample_student.id,
            duration_minutes=25.0
        )
        db.add(session)
        db.commit()
        
        repr_str = repr(session)
        assert "StudySession" in repr_str
        assert "25" in repr_str


class TestStudyStreak:
    """Test StudyStreak model."""
    
    def test_create_study_streak(self, db, sample_student):
        """Test creating a study streak."""
        streak = StudyStreak(
            student_id=sample_student.id,
            current_streak_days=5,
            longest_streak_days=10,
            last_study_date=datetime.utcnow()
        )
        db.add(streak)
        db.commit()
        db.refresh(streak)
        
        assert streak.id is not None
        assert streak.student_id == sample_student.id
        assert streak.current_streak_days == 5
        assert streak.longest_streak_days == 10
        assert streak.last_study_date is not None
        assert streak.student == sample_student
    
    def test_study_streak_defaults(self, db, sample_student):
        """Test study streak default values."""
        streak = StudyStreak(
            student_id=sample_student.id
        )
        db.add(streak)
        db.commit()
        db.refresh(streak)
        
        assert streak.current_streak_days == 0
        assert streak.longest_streak_days == 0
        assert streak.last_study_date is None
    
    def test_study_streak_unique_student(self, db, sample_student):
        """Test that each student can only have one streak."""
        streak1 = StudyStreak(student_id=sample_student.id)
        db.add(streak1)
        db.commit()
        
        # Try to create another streak for the same student
        streak2 = StudyStreak(student_id=sample_student.id)
        db.add(streak2)
        
        with pytest.raises(Exception):  # Should raise integrity error
            db.commit()
    
    def test_study_streak_repr(self, db, sample_student):
        """Test study streak string representation."""
        streak = StudyStreak(
            student_id=sample_student.id,
            current_streak_days=7
        )
        db.add(streak)
        db.commit()
        
        repr_str = repr(streak)
        assert "StudyStreak" in repr_str
        assert "7" in repr_str
