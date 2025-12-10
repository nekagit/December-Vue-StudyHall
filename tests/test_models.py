import pytest
from datetime import datetime
from backend.models import Student, Material
import hashlib


class TestStudent:
    """Test Student model."""
    
    def test_create_student(self, db):
        """Test creating a student."""
        password_hash = hashlib.sha256("password123".encode()).hexdigest()
        student = Student(
            email="student@example.com",
            name="John Doe",
            password_hash=password_hash
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        
        assert student.id is not None
        assert student.email == "student@example.com"
        assert student.name == "John Doe"
        assert student.is_active is True
        assert student.created_at is not None
        assert isinstance(student.created_at, datetime)
    
    def test_student_repr(self, db):
        """Test student string representation."""
        password_hash = hashlib.sha256("password".encode()).hexdigest()
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=password_hash
        )
        db.add(student)
        db.commit()
        
        repr_str = repr(student)
        assert "Student" in repr_str
        assert "test@example.com" in repr_str
        assert "Test User" in repr_str
    
    def test_student_unique_email(self, db):
        """Test that email must be unique."""
        password_hash = hashlib.sha256("password".encode()).hexdigest()
        student1 = Student(
            email="unique@example.com",
            name="User 1",
            password_hash=password_hash
        )
        db.add(student1)
        db.commit()
        
        student2 = Student(
            email="unique@example.com",
            name="User 2",
            password_hash=password_hash
        )
        db.add(student2)
        
        with pytest.raises(Exception):  # Should raise integrity error
            db.commit()
    
    def test_student_email_indexed(self, db):
        """Test that email is indexed for faster lookups."""
        # This is more of a schema test - verify the column has index=True
        student_table = Student.__table__
        email_column = student_table.columns.get("email")
        assert email_column.index is True or any(
            idx.columns.values()[0].name == "email" 
            for idx in student_table.indexes
        )
    
    def test_student_default_is_active(self, db):
        """Test that is_active defaults to True."""
        password_hash = hashlib.sha256("password".encode()).hexdigest()
        student = Student(
            email="active@example.com",
            name="Active User",
            password_hash=password_hash
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        
        assert student.is_active is True
    
    def test_student_set_is_active_false(self, db):
        """Test setting is_active to False."""
        password_hash = hashlib.sha256("password".encode()).hexdigest()
        student = Student(
            email="inactive@example.com",
            name="Inactive User",
            password_hash=password_hash,
            is_active=False
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        
        assert student.is_active is False
    
    def test_student_created_at_timestamp(self, db):
        """Test that created_at is automatically set."""
        password_hash = hashlib.sha256("password".encode()).hexdigest()
        
        student = Student(
            email="timestamp@example.com",
            name="Timestamp User",
            password_hash=password_hash
        )
        db.add(student)
        db.commit()
        db.refresh(student)
        
        assert student.created_at is not None
        assert isinstance(student.created_at, datetime)


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
        assert material.notion_url == "https://notion.so/test"
        assert material.created_at is not None
        assert isinstance(material.created_at, datetime)
    
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
    
    def test_material_minimal_fields(self, db):
        """Test creating material with only required fields."""
        material = Material(title="Minimal Material")
        db.add(material)
        db.commit()
        db.refresh(material)
        
        assert material.id is not None
        assert material.title == "Minimal Material"
        assert material.content is None
        assert material.category is None
        assert material.order_index == 0  # Default value
        assert material.notion_page_id is None
        assert material.notion_url is None
    
    def test_material_default_order_index(self, db):
        """Test that order_index defaults to 0."""
        material = Material(title="Test Material")
        db.add(material)
        db.commit()
        db.refresh(material)
        
        assert material.order_index == 0
    
    def test_material_unique_notion_page_id(self, db):
        """Test that notion_page_id must be unique."""
        material1 = Material(
            title="Material 1",
            notion_page_id="notion-123"
        )
        db.add(material1)
        db.commit()
        
        material2 = Material(
            title="Material 2",
            notion_page_id="notion-123"
        )
        db.add(material2)
        
        with pytest.raises(Exception):  # Should raise integrity error
            db.commit()
    
    def test_material_notion_page_id_can_be_none(self, db):
        """Test that multiple materials can have None notion_page_id."""
        material1 = Material(title="Material 1")
        material2 = Material(title="Material 2")
        
        db.add_all([material1, material2])
        db.commit()
        
        assert material1.notion_page_id is None
        assert material2.notion_page_id is None
    
    def test_material_title_indexed(self, db):
        """Test that title is indexed for faster searches."""
        material_table = Material.__table__
        title_column = material_table.columns.get("title")
        assert title_column.index is True or any(
            idx.columns.values()[0].name == "title" 
            for idx in material_table.indexes
        )
    
    def test_material_created_at_timestamp(self, db):
        """Test that created_at is automatically set."""
        material = Material(title="Timestamp Test")
        db.add(material)
        db.commit()
        db.refresh(material)
        
        assert material.created_at is not None
        assert isinstance(material.created_at, datetime)
    
    def test_material_updated_at_on_update(self, db):
        """Test that updated_at is set when material is updated."""
        material = Material(title="Original Title")
        db.add(material)
        db.commit()
        db.refresh(material)
        
        assert material.updated_at is None
        
        material.title = "Updated Title"
        db.commit()
        db.refresh(material)
        
        assert material.updated_at is not None
        assert isinstance(material.updated_at, datetime)
    
    def test_material_long_content(self, db):
        """Test material with very long content."""
        long_content = "A" * 10000
        material = Material(
            title="Long Content Material",
            content=long_content
        )
        db.add(material)
        db.commit()
        db.refresh(material)
        
        assert material.content == long_content
        assert len(material.content) == 10000
    
    def test_material_ordering(self, db):
        """Test materials can be ordered by order_index."""
        materials = [
            Material(title="Third", order_index=3),
            Material(title="First", order_index=1),
            Material(title="Second", order_index=2),
        ]
        db.add_all(materials)
        db.commit()
        
        # Query ordered by order_index
        ordered = db.query(Material).order_by(Material.order_index).all()
        assert ordered[0].title == "First"
        assert ordered[1].title == "Second"
        assert ordered[2].title == "Third"
    
    def test_material_category_filtering(self, db):
        """Test filtering materials by category."""
        materials = [
            Material(title="Python 1", category="Python"),
            Material(title="Python 2", category="Python"),
            Material(title="JS 1", category="JavaScript"),
        ]
        db.add_all(materials)
        db.commit()
        
        python_materials = db.query(Material).filter(Material.category == "Python").all()
        assert len(python_materials) == 2
        assert all(m.category == "Python" for m in python_materials)
    
    def test_material_without_category(self, db):
        """Test material without category."""
        material = Material(title="No Category Material")
        db.add(material)
        db.commit()
        db.refresh(material)
        
        assert material.category is None
    
    def test_material_notion_url_without_page_id(self, db):
        """Test material can have notion_url without notion_page_id."""
        material = Material(
            title="External Link",
            notion_url="https://notion.so/external"
        )
        db.add(material)
        db.commit()
        db.refresh(material)
        
        assert material.notion_url == "https://notion.so/external"
        assert material.notion_page_id is None
