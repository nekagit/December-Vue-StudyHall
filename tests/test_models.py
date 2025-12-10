import pytest
from datetime import datetime
from backend.models import Student, Material, Bookmark, Progress
from backend.services.auth import hash_password


class TestStudentModel:
    """Test Student model."""
    
    def test_create_student(self, db_session):
        """Test creating a student."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        db_session.commit()
        db_session.refresh(student)
        
        assert student.id is not None
        assert student.email == "test@example.com"
        assert student.name == "Test User"
        assert student.is_active is True
        assert student.created_at is not None
    
    def test_student_unique_email(self, db_session):
        """Test that email must be unique."""
        student1 = Student(
            email="test@example.com",
            name="User 1",
            password_hash=hash_password("password123")
        )
        db_session.add(student1)
        db_session.commit()
        
        student2 = Student(
            email="test@example.com",
            name="User 2",
            password_hash=hash_password("password123")
        )
        db_session.add(student2)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()
    
    def test_student_repr(self, db_session):
        """Test student string representation."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        db_session.commit()
        
        repr_str = repr(student)
        assert "Student" in repr_str
        assert "test@example.com" in repr_str


class TestMaterialModel:
    """Test Material model."""
    
    def test_create_material(self, db_session):
        """Test creating a material."""
        material = Material(
            title="Test Material",
            content="This is test content",
            category="Python",
            order_index=1
        )
        db_session.add(material)
        db_session.commit()
        db_session.refresh(material)
        
        assert material.id is not None
        assert material.title == "Test Material"
        assert material.content == "This is test content"
        assert material.category == "Python"
        assert material.order_index == 1
        assert material.created_at is not None
    
    def test_material_optional_fields(self, db_session):
        """Test creating material with optional fields."""
        material = Material(
            title="Minimal Material",
            notion_page_id="notion-123",
            notion_url="https://notion.so/page-123",
            category="JavaScript"
        )
        db_session.add(material)
        db_session.commit()
        db_session.refresh(material)
        
        assert material.id is not None
        assert material.title == "Minimal Material"
        assert material.notion_page_id == "notion-123"
        assert material.notion_url == "https://notion.so/page-123"
        assert material.category == "JavaScript"
    
    def test_material_unique_notion_page_id(self, db_session):
        """Test that notion_page_id must be unique."""
        material1 = Material(
            title="Material 1",
            notion_page_id="notion-123"
        )
        db_session.add(material1)
        db_session.commit()
        
        material2 = Material(
            title="Material 2",
            notion_page_id="notion-123"
        )
        db_session.add(material2)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()
    
    def test_material_repr(self, db_session):
        """Test material string representation."""
        material = Material(
            title="Test Material",
            content="Content"
        )
        db_session.add(material)
        db_session.commit()
        
        repr_str = repr(material)
        assert "Material" in repr_str
        assert "Test Material" in repr_str


class TestBookmarkModel:
    """Test Bookmark model."""
    
    def test_create_bookmark(self, db_session):
        """Test creating a bookmark."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        db_session.commit()
        
        bookmark = Bookmark(
            student_id=student.id,
            material_id=material.id
        )
        db_session.add(bookmark)
        db_session.commit()
        db_session.refresh(bookmark)
        
        assert bookmark.id is not None
        assert bookmark.student_id == student.id
        assert bookmark.material_id == material.id
        assert bookmark.created_at is not None
    
    def test_bookmark_relationships(self, db_session):
        """Test bookmark relationships to student and material."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        db_session.commit()
        
        bookmark = Bookmark(
            student_id=student.id,
            material_id=material.id
        )
        db_session.add(bookmark)
        db_session.commit()
        
        # Test relationships
        assert bookmark.student.email == "test@example.com"
        assert bookmark.material.title == "Test Material"
        assert bookmark in student.bookmarks
        assert bookmark in material.bookmarks
    
    def test_bookmark_repr(self, db_session):
        """Test bookmark string representation."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        db_session.commit()
        
        bookmark = Bookmark(
            student_id=student.id,
            material_id=material.id
        )
        db_session.add(bookmark)
        db_session.commit()
        
        repr_str = repr(bookmark)
        assert "Bookmark" in repr_str
        assert str(student.id) in repr_str
        assert str(material.id) in repr_str


class TestProgressModel:
    """Test Progress model."""
    
    def test_create_progress(self, db_session):
        """Test creating a progress record."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        db_session.commit()
        
        progress = Progress(
            student_id=student.id,
            material_id=material.id,
            status="in_progress",
            progress_percentage=50.0
        )
        db_session.add(progress)
        db_session.commit()
        db_session.refresh(progress)
        
        assert progress.id is not None
        assert progress.student_id == student.id
        assert progress.material_id == material.id
        assert progress.status == "in_progress"
        assert progress.progress_percentage == 50.0
        assert progress.last_accessed_at is not None
    
    def test_progress_default_values(self, db_session):
        """Test progress default values."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        db_session.commit()
        
        progress = Progress(
            student_id=student.id,
            material_id=material.id
        )
        db_session.add(progress)
        db_session.commit()
        db_session.refresh(progress)
        
        assert progress.status == "not_started"
        assert progress.progress_percentage == 0.0
        assert progress.completed_at is None
    
    def test_progress_completed(self, db_session):
        """Test progress with completed status."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        db_session.commit()
        
        progress = Progress(
            student_id=student.id,
            material_id=material.id,
            status="completed",
            progress_percentage=100.0
        )
        db_session.add(progress)
        db_session.commit()
        db_session.refresh(progress)
        
        assert progress.status == "completed"
        assert progress.progress_percentage == 100.0
    
    def test_progress_relationships(self, db_session):
        """Test progress relationships to student and material."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        db_session.commit()
        
        progress = Progress(
            student_id=student.id,
            material_id=material.id,
            status="in_progress",
            progress_percentage=50.0
        )
        db_session.add(progress)
        db_session.commit()
        
        # Test relationships
        assert progress.student.email == "test@example.com"
        assert progress.material.title == "Test Material"
        assert progress in student.progress_records
        assert progress in material.progress_records
    
    def test_progress_repr(self, db_session):
        """Test progress string representation."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        db_session.commit()
        
        progress = Progress(
            student_id=student.id,
            material_id=material.id,
            status="in_progress"
        )
        db_session.add(progress)
        db_session.commit()
        
        repr_str = repr(progress)
        assert "Progress" in repr_str
        assert "in_progress" in repr_str
