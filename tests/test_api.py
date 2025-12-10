import pytest
import json
from backend.models import Student, Material, Bookmark, Progress
from backend.services.auth import hash_password
from backend.services.session import create_session


class TestAuthEndpoints:
    """Test authentication endpoints."""
    
    def test_register_success(self, client, db):
        """Test successful registration."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "name": "New User",
                "password": "password123"
            }
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert "student" in data
        assert data["student"]["email"] == "newuser@example.com"
        assert data["student"]["name"] == "New User"
        assert "session_token" in response.headers.get("Set-Cookie", "")
    
    def test_register_duplicate_email(self, client, db):
        """Test registration with duplicate email."""
        # Create first user
        client.post(
            "/api/auth/register",
            json={
                "email": "duplicate@example.com",
                "name": "User 1",
                "password": "password1"
            }
        )
        
        # Try to register again with same email
        response = client.post(
            "/api/auth/register",
            json={
                "email": "duplicate@example.com",
                "name": "User 2",
                "password": "password2"
            }
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "already registered" in data["error"].lower()
    
    def test_register_missing_fields(self, client):
        """Test registration with missing fields."""
        response = client.post(
            "/api/auth/register",
            json={"email": "test@example.com"}
        )
        
        # Should handle missing fields gracefully
        assert response.status_code in [400, 500]
    
    def test_login_success(self, client, db):
        """Test successful login."""
        # Create a student
        student = Student(
            email="login@example.com",
            name="Login User",
            password_hash=hash_password("password123")
        )
        db.add(student)
        db.commit()
        
        response = client.post(
            "/api/auth/login",
            json={
                "email": "login@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["student"]["email"] == "login@example.com"
        assert "session_token" in response.headers.get("Set-Cookie", "")
    
    def test_login_invalid_credentials(self, client, db):
        """Test login with invalid credentials."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("correctpassword")
        )
        db.add(student)
        db.commit()
        
        response = client.post(
            "/api/auth/login",
            json={
                "email": "test@example.com",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        response = client.post(
            "/api/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password"
            }
        )
        
        assert response.status_code == 401
    
    def test_logout(self, client, db, sample_student):
        """Test logout."""
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.post("/api/auth/logout")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
    
    def test_get_current_user_authenticated(self, client, db, sample_student):
        """Test getting current user when authenticated."""
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.get("/api/auth/me")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == sample_student.id
        assert data["email"] == sample_student.email
        assert data["name"] == sample_student.name
    
    def test_get_current_user_unauthenticated(self, client):
        """Test getting current user when not authenticated."""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data


class TestMaterialsEndpoints:
    """Test materials endpoints."""
    
    def test_get_materials_authenticated(self, client, db, sample_student, sample_material):
        """Test getting materials when authenticated."""
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.get("/api/materials")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == sample_material.id
        assert data[0]["title"] == sample_material.title
    
    def test_get_materials_unauthenticated(self, client):
        """Test getting materials when not authenticated."""
        response = client.get("/api/materials")
        
        assert response.status_code == 401
    
    def test_get_materials_with_search(self, client, db, sample_student):
        """Test getting materials with search query."""
        material1 = Material(title="Python Basics", content="Learn Python")
        material2 = Material(title="JavaScript Advanced", content="Learn JS")
        db.add_all([material1, material2])
        db.commit()
        
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.get("/api/materials?search=Python")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert "Python" in data[0]["title"]
    
    def test_get_materials_with_category(self, client, db, sample_student):
        """Test getting materials filtered by category."""
        material1 = Material(title="Python 1", category="Python")
        material2 = Material(title="JS 1", category="JavaScript")
        db.add_all([material1, material2])
        db.commit()
        
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.get("/api/materials?category=Python")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["category"] == "Python"
    
    def test_get_material_detail(self, client, db, sample_student, sample_material):
        """Test getting a specific material."""
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.get(f"/api/materials/{sample_material.id}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == sample_material.id
        assert data["title"] == sample_material.title
        assert "is_bookmarked" in data
        assert "progress" in data
    
    def test_get_material_not_found(self, client, db, sample_student):
        """Test getting a non-existent material."""
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.get("/api/materials/99999")
        
        assert response.status_code == 404
    
    def test_get_categories(self, client, db, sample_student):
        """Test getting all categories."""
        Material(title="Python 1", category="Python")
        Material(title="Python 2", category="Python")
        Material(title="JS 1", category="JavaScript")
        db.commit()
        
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.get("/api/materials/categories")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert "Python" in data
        assert "JavaScript" in data


class TestBookmarksEndpoints:
    """Test bookmarks endpoints."""
    
    def test_get_bookmarks(self, client, db, sample_student, sample_material):
        """Test getting all bookmarks."""
        bookmark = Bookmark(student_id=sample_student.id, material_id=sample_material.id)
        db.add(bookmark)
        db.commit()
        
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.get("/api/bookmarks")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["material_id"] == sample_material.id
    
    def test_create_bookmark(self, client, db, sample_student, sample_material):
        """Test creating a bookmark."""
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.post(
            "/api/bookmarks",
            json={"material_id": sample_material.id}
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["bookmark"]["material_id"] == sample_material.id
    
    def test_create_duplicate_bookmark(self, client, db, sample_student, sample_material):
        """Test creating a duplicate bookmark."""
        bookmark = Bookmark(student_id=sample_student.id, material_id=sample_material.id)
        db.add(bookmark)
        db.commit()
        
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.post(
            "/api/bookmarks",
            json={"material_id": sample_material.id}
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_create_bookmark_invalid_material(self, client, db, sample_student):
        """Test creating bookmark for non-existent material."""
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.post(
            "/api/bookmarks",
            json={"material_id": 99999}
        )
        
        assert response.status_code == 404
    
    def test_delete_bookmark(self, client, db, sample_student, sample_material):
        """Test deleting a bookmark."""
        bookmark = Bookmark(student_id=sample_student.id, material_id=sample_material.id)
        db.add(bookmark)
        db.commit()
        
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.delete(f"/api/bookmarks/{bookmark.id}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
    
    def test_delete_bookmark_by_material(self, client, db, sample_student, sample_material):
        """Test deleting bookmark by material ID."""
        bookmark = Bookmark(student_id=sample_student.id, material_id=sample_material.id)
        db.add(bookmark)
        db.commit()
        
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.delete(f"/api/bookmarks/material/{sample_material.id}")
        
        assert response.status_code == 200


class TestProgressEndpoints:
    """Test progress endpoints."""
    
    def test_get_progress(self, client, db, sample_student, sample_material):
        """Test getting all progress records."""
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id,
            status="in_progress",
            progress_percentage=50.0
        )
        db.add(progress)
        db.commit()
        
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.get("/api/progress")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["status"] == "in_progress"
    
    def test_get_material_progress(self, client, db, sample_student, sample_material):
        """Test getting progress for a specific material."""
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id,
            status="completed",
            progress_percentage=100.0
        )
        db.add(progress)
        db.commit()
        
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.get(f"/api/progress/material/{sample_material.id}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "completed"
        assert data["progress_percentage"] == 100.0
    
    def test_get_material_progress_not_found(self, client, db, sample_student, sample_material):
        """Test getting progress for material without progress record."""
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.get(f"/api/progress/material/{sample_material.id}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "not_started"
        assert data["progress_percentage"] == 0.0
    
    def test_update_progress_create(self, client, db, sample_student, sample_material):
        """Test creating a new progress record."""
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.post(
            f"/api/progress/material/{sample_material.id}",
            json={
                "status": "in_progress",
                "progress_percentage": 25.0
            }
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["progress"]["status"] == "in_progress"
        assert data["progress"]["progress_percentage"] == 25.0
    
    def test_update_progress_update(self, client, db, sample_student, sample_material):
        """Test updating an existing progress record."""
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id,
            status="in_progress",
            progress_percentage=50.0
        )
        db.add(progress)
        db.commit()
        
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.put(
            f"/api/progress/material/{sample_material.id}",
            json={
                "status": "completed",
                "progress_percentage": 100.0
            }
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["progress"]["status"] == "completed"
        assert data["progress"]["progress_percentage"] == 100.0
    
    def test_update_progress_invalid_status(self, client, db, sample_student, sample_material):
        """Test updating progress with invalid status."""
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.post(
            f"/api/progress/material/{sample_material.id}",
            json={
                "status": "invalid_status",
                "progress_percentage": 50.0
            }
        )
        
        assert response.status_code == 400
    
    def test_update_progress_invalid_percentage(self, client, db, sample_student, sample_material):
        """Test updating progress with invalid percentage."""
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.post(
            f"/api/progress/material/{sample_material.id}",
            json={
                "status": "in_progress",
                "progress_percentage": 150.0  # Invalid: > 100
            }
        )
        
        assert response.status_code == 400


class TestDashboardEndpoints:
    """Test dashboard endpoints."""
    
    def test_get_dashboard_stats(self, client, db, sample_student, sample_material):
        """Test getting dashboard statistics."""
        # Create some test data
        bookmark = Bookmark(student_id=sample_student.id, material_id=sample_material.id)
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id,
            status="completed"
        )
        db.add_all([bookmark, progress])
        db.commit()
        
        token = create_session(sample_student.id)
        client.set_cookie('localhost', 'session_token', token)
        
        response = client.get("/api/dashboard/stats")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "total_materials" in data
        assert "total_bookmarks" in data
        assert "completed_materials" in data
        assert "in_progress_materials" in data
        assert "recent_bookmarks" in data
        assert "recent_progress" in data
        assert data["total_bookmarks"] == 1
        assert data["completed_materials"] == 1
