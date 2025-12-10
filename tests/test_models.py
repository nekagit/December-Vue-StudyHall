import pytest
from datetime import datetime
from backend.models import Student, Material, Bookmark, Progress
from backend.services.auth import create_student


class TestStudentModel:
    """Test Student model."""
    
    def test_create_student(self, db_session):
        """Test creating a student."""
        student = Student(
            email="test@example.com",
            name="Test Student",
            password_hash="hashed_password"
        )
        db_session.add(student)
        db_session.commit()
        db_session.refresh(student)
        
        assert student.id is not None
        assert student.email == "test@example.com"
        assert student.name == "Test Student"
        assert student.password_hash == "hashed_password"
        assert student.is_active is True
        assert student.created_at is not None
    
    def test_student_unique_email(self, db_session):
        """Test that email must be unique."""
        student1 = Student(
            email="test@example.com",
            name="Student 1",
            password_hash="hash1"
        )
        db_session.add(student1)
        db_session.commit()
        
        student2 = Student(
            email="test@example.com",
            name="Student 2",
            password_hash="hash2"
        )
        db_session.add(student2)
        
        with pytest.raises(Exception):  # IntegrityError or similar
            db_session.commit()
    
    def test_student_repr(self, db_session):
        """Test student string representation."""
        student = Student(
            email="test@example.com",
            name="Test Student",
            password_hash="hash"
        )
        db_session.add(student)
        db_session.commit()
        
        repr_str = repr(student)
        assert "Student" in repr_str
        assert "test@example.com" in repr_str
        assert "Test Student" in repr_str


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
    
    def test_material_with_notion_fields(self, db_session):
        """Test creating material with Notion fields."""
        material = Material(
            title="Notion Material",
            content="Content from Notion",
            notion_page_id="notion_page_123",
            notion_url="https://notion.so/page/123",
            category="Web Dev"
        )
        db_session.add(material)
        db_session.commit()
        db_session.refresh(material)
        
        assert material.notion_page_id == "notion_page_123"
        assert material.notion_url == "https://notion.so/page/123"
    
    def test_material_unique_notion_page_id(self, db_session):
        """Test that notion_page_id must be unique."""
        material1 = Material(
            title="Material 1",
            notion_page_id="notion_123"
        )
        db_session.add(material1)
        db_session.commit()
        
        material2 = Material(
            title="Material 2",
            notion_page_id="notion_123"
        )
        db_session.add(material2)
        
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()
    
    def test_material_repr(self, db_session):
        """Test material string representation."""
        material = Material(
            title="A" * 100,  # Long title
            content="Content"
        )
        db_session.add(material)
        db_session.commit()
        
        repr_str = repr(material)
        assert "Material" in repr_str
        # Should truncate long titles in repr
        assert len(repr_str) < 200


class TestBookmarkModel:
    """Test Bookmark model."""
    
    def test_create_bookmark(self, db_session, sample_student, sample_material):
        """Test creating a bookmark."""
        bookmark = Bookmark(
            student_id=sample_student.id,
            material_id=sample_material.id
        )
        db_session.add(bookmark)
        db_session.commit()
        db_session.refresh(bookmark)
        
        assert bookmark.id is not None
        assert bookmark.student_id == sample_student.id
        assert bookmark.material_id == sample_material.id
        assert bookmark.created_at is not None
    
    def test_bookmark_relationships(self, db_session, sample_student, sample_material):
        """Test bookmark relationships."""
        bookmark = Bookmark(
            student_id=sample_student.id,
            material_id=sample_material.id
        )
        db_session.add(bookmark)
        db_session.commit()
        
        # Test relationship to student
        assert bookmark.student.id == sample_student.id
        assert bookmark.student.email == sample_student.email
        
        # Test relationship to material
        assert bookmark.material.id == sample_material.id
        assert bookmark.material.title == sample_material.title
    
    def test_bookmark_repr(self, db_session, sample_student, sample_material):
        """Test bookmark string representation."""
        bookmark = Bookmark(
            student_id=sample_student.id,
            material_id=sample_material.id
        )
        db_session.add(bookmark)
        db_session.commit()
        
        repr_str = repr(bookmark)
        assert "Bookmark" in repr_str
        assert str(sample_student.id) in repr_str
        assert str(sample_material.id) in repr_str
    
    def test_student_bookmarks_backref(self, db_session, sample_student, sample_material):
        """Test that student has bookmarks backref."""
        bookmark = Bookmark(
            student_id=sample_student.id,
            material_id=sample_material.id
        )
        db_session.add(bookmark)
        db_session.commit()
        
        db_session.refresh(sample_student)
        assert len(sample_student.bookmarks) == 1
        assert sample_student.bookmarks[0].id == bookmark.id
    
    def test_material_bookmarks_backref(self, db_session, sample_student, sample_material):
        """Test that material has bookmarks backref."""
        bookmark = Bookmark(
            student_id=sample_student.id,
            material_id=sample_material.id
        )
        db_session.add(bookmark)
        db_session.commit()
        
        db_session.refresh(sample_material)
        assert len(sample_material.bookmarks) == 1
        assert sample_material.bookmarks[0].id == bookmark.id


class TestProgressModel:
    """Test Progress model."""
    
    def test_create_progress(self, db_session, sample_student, sample_material):
        """Test creating a progress record."""
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id,
            status="in_progress",
            progress_percentage=50.0
        )
        db_session.add(progress)
        db_session.commit()
        db_session.refresh(progress)
        
        assert progress.id is not None
        assert progress.student_id == sample_student.id
        assert progress.material_id == sample_material.id
        assert progress.status == "in_progress"
        assert progress.progress_percentage == 50.0
        assert progress.last_accessed_at is not None
        assert progress.created_at is not None
    
    def test_progress_default_values(self, db_session, sample_student, sample_material):
        """Test progress default values."""
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id
        )
        db_session.add(progress)
        db_session.commit()
        db_session.refresh(progress)
        
        assert progress.status == "not_started"
        assert progress.progress_percentage == 0.0
        assert progress.completed_at is None
    
    def test_progress_completed(self, db_session, sample_student, sample_material):
        """Test progress with completed status."""
        from datetime import datetime
        
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id,
            status="completed",
            progress_percentage=100.0,
            completed_at=datetime.utcnow()
        )
        db_session.add(progress)
        db_session.commit()
        db_session.refresh(progress)
        
        assert progress.status == "completed"
        assert progress.progress_percentage == 100.0
        assert progress.completed_at is not None
    
    def test_progress_relationships(self, db_session, sample_student, sample_material):
        """Test progress relationships."""
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id,
            status="in_progress"
        )
        db_session.add(progress)
        db_session.commit()
        
        # Test relationship to student
        assert progress.student.id == sample_student.id
        assert progress.student.email == sample_student.email
        
        # Test relationship to material
        assert progress.material.id == sample_material.id
        assert progress.material.title == sample_material.title
    
    def test_progress_repr(self, db_session, sample_student, sample_material):
        """Test progress string representation."""
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id,
            status="completed"
        )
        db_session.add(progress)
        db_session.commit()
        
        repr_str = repr(progress)
        assert "Progress" in repr_str
        assert str(sample_student.id) in repr_str
        assert str(sample_material.id) in repr_str
        assert "completed" in repr_str
    
    def test_student_progress_backref(self, db_session, sample_student, sample_material):
        """Test that student has progress_records backref."""
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id
        )
        db_session.add(progress)
        db_session.commit()
        
        db_session.refresh(sample_student)
        assert len(sample_student.progress_records) == 1
        assert sample_student.progress_records[0].id == progress.id
    
    def test_material_progress_backref(self, db_session, sample_student, sample_material):
        """Test that material has progress_records backref."""
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id
        )
        db_session.add(progress)
        db_session.commit()
        
        db_session.refresh(sample_material)
        assert len(sample_material.progress_records) == 1
        assert sample_material.progress_records[0].id == progress.id


class TestModelRelationships:
    """Test relationships between models."""
    
    def test_student_material_through_bookmarks(self, db_session):
        """Test student-material relationship through bookmarks."""
        student = create_student(
            db_session,
            email="test@example.com",
            name="Test Student",
            password="password123"
        )
        
        material1 = Material(title="Material 1", category="Python")
        material2 = Material(title="Material 2", category="JavaScript")
        db_session.add_all([material1, material2])
        db_session.commit()
        
        bookmark1 = Bookmark(student_id=student.id, material_id=material1.id)
        bookmark2 = Bookmark(student_id=student.id, material_id=material2.id)
        db_session.add_all([bookmark1, bookmark2])
        db_session.commit()
        
        db_session.refresh(student)
        assert len(student.bookmarks) == 2
        assert {b.material_id for b in student.bookmarks} == {material1.id, material2.id}
    
    def test_student_material_through_progress(self, db_session):
        """Test student-material relationship through progress."""
        student = create_student(
            db_session,
            email="test@example.com",
            name="Test Student",
            password="password123"
        )
        
        material1 = Material(title="Material 1", category="Python")
        material2 = Material(title="Material 2", category="JavaScript")
        db_session.add_all([material1, material2])
        db_session.commit()
        
        progress1 = Progress(
            student_id=student.id,
            material_id=material1.id,
            status="completed"
        )
        progress2 = Progress(
            student_id=student.id,
            material_id=material2.id,
            status="in_progress"
        )
        db_session.add_all([progress1, progress2])
        db_session.commit()
        
        db_session.refresh(student)
        assert len(student.progress_records) == 2
        assert {p.material_id for p in student.progress_records} == {material1.id, material2.id}
