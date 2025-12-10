import pytest
from datetime import datetime
from backend.models import Student, Material, MaterialProgress, Bookmark

def test_student_model(db_session):
    """Test Student model creation and attributes."""
    student = Student(
        email="test@example.com",
        name="Test User",
        password_hash="hashed_password"
    )
    db_session.add(student)
    db_session.commit()
    db_session.refresh(student)
    
    assert student.id is not None
    assert student.email == "test@example.com"
    assert student.name == "Test User"
    assert student.password_hash == "hashed_password"
    assert student.is_active is True
    assert student.created_at is not None

def test_material_model(db_session):
    """Test Material model creation and attributes."""
    material = Material(
        title="Test Material",
        content="Test content",
        category="Python",
        order_index=1
    )
    db_session.add(material)
    db_session.commit()
    db_session.refresh(material)
    
    assert material.id is not None
    assert material.title == "Test Material"
    assert material.content == "Test content"
    assert material.category == "Python"
    assert material.order_index == 1
    assert material.created_at is not None

def test_material_progress_model(db_session):
    """Test MaterialProgress model creation."""
    student = Student(
        email="test@example.com",
        name="Test User",
        password_hash="hash"
    )
    material = Material(title="Test Material", content="Content")
    db_session.add_all([student, material])
    db_session.commit()
    
    progress = MaterialProgress(
        student_id=student.id,
        material_id=material.id,
        is_completed=False,
        progress_percentage=50
    )
    db_session.add(progress)
    db_session.commit()
    db_session.refresh(progress)
    
    assert progress.id is not None
    assert progress.student_id == student.id
    assert progress.material_id == material.id
    assert progress.is_completed is False
    assert progress.progress_percentage == 50

def test_bookmark_model(db_session):
    """Test Bookmark model creation."""
    student = Student(
        email="test@example.com",
        name="Test User",
        password_hash="hash"
    )
    material = Material(title="Test Material", content="Content")
    db_session.add_all([student, material])
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
