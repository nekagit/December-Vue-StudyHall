import pytest
import json
from backend.models import Student, Material
from backend.services.auth import create_student
from backend.services.session import create_session

def test_register_endpoint(client, db_session, sample_student_data):
    """Test user registration endpoint."""
    response = client.post(
        "/api/auth/register",
        json=sample_student_data,
        content_type="application/json"
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert data["student"]["email"] == sample_student_data["email"]
    assert data["student"]["name"] == sample_student_data["name"]
    assert "session_token" in response.headers.get("Set-Cookie", "")

def test_register_duplicate_email(client, db_session, sample_student_data):
    """Test registration with duplicate email."""
    # Register first time
    client.post(
        "/api/auth/register",
        json=sample_student_data,
        content_type="application/json"
    )
    
    # Try to register again
    response = client.post(
        "/api/auth/register",
        json=sample_student_data,
        content_type="application/json"
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data

def test_login_endpoint(client, db_session, sample_student_data):
    """Test login endpoint."""
    # Register first
    client.post(
        "/api/auth/register",
        json=sample_student_data,
        content_type="application/json"
    )
    
    # Login
    response = client.post(
        "/api/auth/login",
        json={
            "email": sample_student_data["email"],
            "password": sample_student_data["password"]
        },
        content_type="application/json"
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True
    assert data["student"]["email"] == sample_student_data["email"]

def test_login_invalid_credentials(client, db_session):
    """Test login with invalid credentials."""
    response = client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        },
        content_type="application/json"
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert "error" in data

def test_logout_endpoint(client, db_session, sample_student_data):
    """Test logout endpoint."""
    # Register and login
    client.post(
        "/api/auth/register",
        json=sample_student_data,
        content_type="application/json"
    )
    
    response = client.post(
        "/api/auth/logout",
        content_type="application/json"
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["success"] is True

def test_get_current_user_authenticated(client, db_session, sample_student_data):
    """Test getting current user when authenticated."""
    # Register
    register_response = client.post(
        "/api/auth/register",
        json=sample_student_data,
        content_type="application/json"
    )
    
    # Get session token from cookie
    cookies = register_response.headers.getlist("Set-Cookie")
    session_token = None
    for cookie in cookies:
        if "session_token" in cookie:
            session_token = cookie.split("session_token=")[1].split(";")[0]
    
    # Get current user
    client.set_cookie("localhost", "session_token", session_token)
    response = client.get("/api/auth/me")
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["email"] == sample_student_data["email"]
    assert data["name"] == sample_student_data["name"]

def test_get_current_user_unauthenticated(client):
    """Test getting current user when not authenticated."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401

def test_get_materials_authenticated(client, db_session, sample_student_data):
    """Test getting materials when authenticated."""
    # Register and get session
    student = create_student(
        db_session,
        sample_student_data["email"],
        sample_student_data["name"],
        sample_student_data["password"]
    )
    token = create_session(student.id)
    
    # Create some materials
    material1 = Material(title="Material 1", content="Content 1", category="Python")
    material2 = Material(title="Material 2", content="Content 2", category="JavaScript")
    db_session.add_all([material1, material2])
    db_session.commit()
    
    # Get materials
    client.set_cookie("localhost", "session_token", token)
    response = client.get("/api/materials")
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 2
    assert data[0]["title"] in ["Material 1", "Material 2"]

def test_get_materials_unauthenticated(client):
    """Test getting materials when not authenticated."""
    response = client.get("/api/materials")
    assert response.status_code == 401

def test_get_materials_with_search(client, db_session, sample_student_data):
    """Test getting materials with search filter."""
    student = create_student(
        db_session,
        sample_student_data["email"],
        sample_student_data["name"],
        sample_student_data["password"]
    )
    token = create_session(student.id)
    
    material1 = Material(title="Python Basics", content="Learn Python", category="Python")
    material2 = Material(title="JavaScript Advanced", content="Advanced JS", category="JavaScript")
    db_session.add_all([material1, material2])
    db_session.commit()
    
    client.set_cookie("localhost", "session_token", token)
    response = client.get("/api/materials?search=Python")
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert "Python" in data[0]["title"]

def test_get_materials_with_category(client, db_session, sample_student_data):
    """Test getting materials with category filter."""
    student = create_student(
        db_session,
        sample_student_data["email"],
        sample_student_data["name"],
        sample_student_data["password"]
    )
    token = create_session(student.id)
    
    material1 = Material(title="Python Basics", content="Learn Python", category="Python")
    material2 = Material(title="JavaScript Advanced", content="Advanced JS", category="JavaScript")
    db_session.add_all([material1, material2])
    db_session.commit()
    
    client.set_cookie("localhost", "session_token", token)
    response = client.get("/api/materials?category=Python")
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]["category"] == "Python"

def test_get_material_detail(client, db_session, sample_student_data):
    """Test getting a single material detail."""
    student = create_student(
        db_session,
        sample_student_data["email"],
        sample_student_data["name"],
        sample_student_data["password"]
    )
    token = create_session(student.id)
    
    material = Material(title="Test Material", content="Test Content", category="Python")
    db_session.add(material)
    db_session.commit()
    
    client.set_cookie("localhost", "session_token", token)
    response = client.get(f"/api/materials/{material.id}")
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == material.id
    assert data["title"] == "Test Material"
    assert data["content"] == "Test Content"
    assert "progress" in data

def test_get_material_not_found(client, db_session, sample_student_data):
    """Test getting non-existent material."""
    student = create_student(
        db_session,
        sample_student_data["email"],
        sample_student_data["name"],
        sample_student_data["password"]
    )
    token = create_session(student.id)
    
    client.set_cookie("localhost", "session_token", token)
    response = client.get("/api/materials/99999")
    
    assert response.status_code == 404

def test_get_categories(client, db_session, sample_student_data):
    """Test getting categories."""
    student = create_student(
        db_session,
        sample_student_data["email"],
        sample_student_data["name"],
        sample_student_data["password"]
    )
    token = create_session(student.id)
    
    material1 = Material(title="Material 1", content="Content", category="Python")
    material2 = Material(title="Material 2", content="Content", category="JavaScript")
    material3 = Material(title="Material 3", content="Content", category="Python")
    db_session.add_all([material1, material2, material3])
    db_session.commit()
    
    client.set_cookie("localhost", "session_token", token)
    response = client.get("/api/materials/categories")
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "Python" in data
    assert "JavaScript" in data
    assert len(data) == 2
