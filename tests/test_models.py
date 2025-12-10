import pytest
from datetime import datetime
from backend.models.student import Student
from backend.models.material import Material

class TestStudent:
    """Tests for Student model."""
    
    def test_create_student(self, db_session, sample_student_data):
        """Test creating a student."""
        student = Student(
            email=sample_student_data["email"],
            name=sample_student_data["name"],
            password_hash="hashed_password"
        )
        db_session.add(student)
        db_session.commit()
        db_session.refresh(student)
        
        assert student.id is not None
        assert student.email == sample_student_data["email"]
        assert student.name == sample_student_data["name"]
        assert student.password_hash == "hashed_password"
        assert student.is_active is True
        assert student.created_at is not None
    
    def test_student_repr(self, db_session, sample_student_data):
        """Test Student __repr__ method."""
        student = Student(
            email=sample_student_data["email"],
            name=sample_student_data["name"],
            password_hash="hashed_password"
        )
        db_session.add(student)
        db_session.commit()
        
        repr_str = repr(student)
        assert "Student" in repr_str
        assert str(student.id) in repr_str
        assert student.email in repr_str
        assert student.name in repr_str
    
    def test_student_unique_email(self, db_session, sample_student_data):
        """Test that email must be unique."""
        student1 = Student(
            email=sample_student_data["email"],
            name=sample_student_data["name"],
            password_hash="hash1"
        )
        db_session.add(student1)
        db_session.commit()
        
        student2 = Student(
            email=sample_student_data["email"],  # Same email
            name="Another Student",
            password_hash="hash2"
        )
        db_session.add(student2)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()
    
    def test_student_is_active_default(self, db_session, sample_student_data):
        """Test that is_active defaults to True."""
        student = Student(
            email=sample_student_data["email"],
            name=sample_student_data["name"],
            password_hash="hashed_password"
        )
        db_session.add(student)
        db_session.commit()
        
        assert student.is_active is True


class TestMaterial:
    """Tests for Material model."""
    
    def test_create_material(self, db_session, sample_material_data):
        """Test creating a material."""
        material = Material(
            title=sample_material_data["title"],
            content=sample_material_data["content"],
            category=sample_material_data["category"],
            notion_url=sample_material_data["notion_url"],
            notion_page_id=sample_material_data["notion_page_id"]
        )
        db_session.add(material)
        db_session.commit()
        db_session.refresh(material)
        
        assert material.id is not None
        assert material.title == sample_material_data["title"]
        assert material.content == sample_material_data["content"]
        assert material.category == sample_material_data["category"]
        assert material.notion_url == sample_material_data["notion_url"]
        assert material.notion_page_id == sample_material_data["notion_page_id"]
        assert material.order_index == 0
        assert material.created_at is not None
    
    def test_material_repr(self, db_session, sample_material_data):
        """Test Material __repr__ method."""
        material = Material(
            title=sample_material_data["title"],
            content=sample_material_data["content"],
            category=sample_material_data["category"]
        )
        db_session.add(material)
        db_session.commit()
        
        repr_str = repr(material)
        assert "Material" in repr_str
        assert str(material.id) in repr_str
        assert sample_material_data["title"] in repr_str
    
    def test_material_order_index_default(self, db_session):
        """Test that order_index defaults to 0."""
        material = Material(
            title="Test Material",
            content="Content"
        )
        db_session.add(material)
        db_session.commit()
        
        assert material.order_index == 0
    
    def test_material_unique_notion_page_id(self, db_session, sample_material_data):
        """Test that notion_page_id must be unique."""
        material1 = Material(
            title="Material 1",
            content="Content 1",
            notion_page_id=sample_material_data["notion_page_id"]
        )
        db_session.add(material1)
        db_session.commit()
        
        material2 = Material(
            title="Material 2",
            content="Content 2",
            notion_page_id=sample_material_data["notion_page_id"]  # Same notion_page_id
        )
        db_session.add(material2)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()
    
    def test_material_optional_fields(self, db_session):
        """Test that some fields are optional."""
        material = Material(
            title="Minimal Material"
        )
        db_session.add(material)
        db_session.commit()
        
        assert material.id is not None
        assert material.title == "Minimal Material"
        assert material.content is None
        assert material.category is None
        assert material.notion_url is None
        assert material.notion_page_id is None
