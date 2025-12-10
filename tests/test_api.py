import pytest
import json
from unittest.mock import patch, MagicMock
from backend.models import Student, Material, Bookmark, Progress
from backend.services.auth import hash_password, create_student
from backend.services.session import create_session


class TestAuthEndpoints:
    """Test authentication endpoints."""
    
    def test_login_success(self, test_client, db_session):
        """Test successful login."""
        # Create a test student
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        db_session.commit()
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.post(
                "/api/auth/login",
                json={"email": "test@example.com", "password": "password123"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["student"]["email"] == "test@example.com"
        assert "session_token" in response.headers.get("Set-Cookie", "")
    
    def test_login_invalid_email(self, test_client, db_session):
        """Test login with invalid email."""
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.post(
                "/api/auth/login",
                json={"email": "nonexistent@example.com", "password": "password123"}
            )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
    
    def test_login_invalid_password(self, test_client, db_session):
        """Test login with invalid password."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("correctpassword")
        )
        db_session.add(student)
        db_session.commit()
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.post(
                "/api/auth/login",
                json={"email": "test@example.com", "password": "wrongpassword"}
            )
        
        assert response.status_code == 401
    
    def test_register_success(self, test_client, db_session):
        """Test successful registration."""
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.post(
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
        assert data["student"]["email"] == "newuser@example.com"
        
        # Verify student was created in database
        student = db_session.query(Student).filter(Student.email == "newuser@example.com").first()
        assert student is not None
    
    def test_register_duplicate_email(self, test_client, db_session):
        """Test registration with duplicate email."""
        student = Student(
            email="existing@example.com",
            name="Existing User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        db_session.commit()
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.post(
                "/api/auth/register",
                json={
                    "email": "existing@example.com",
                    "name": "New User",
                    "password": "password123"
                }
            )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_register_max_students(self, test_client, db_session):
        """Test registration when max students limit is reached."""
        # Create 30 students
        for i in range(30):
            student = Student(
                email=f"student{i}@example.com",
                name=f"Student {i}",
                password_hash=hash_password("password123")
            )
            db_session.add(student)
        db_session.commit()
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.post(
                "/api/auth/register",
                json={
                    "email": "newuser@example.com",
                    "name": "New User",
                    "password": "password123"
                }
            )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
        assert "30" in data["error"]
    
    def test_logout(self, test_client, db_session):
        """Test logout endpoint."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        db_session.commit()
        
        # Create a session token
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.post(
                "/api/auth/logout",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
    
    def test_get_current_user_success(self, test_client, db_session):
        """Test getting current user when authenticated."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        db_session.commit()
        
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get(
                "/api/auth/me",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
    
    def test_get_current_user_unauthenticated(self, test_client, db_session):
        """Test getting current user when not authenticated."""
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get("/api/auth/me")
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data


class TestMaterialsEndpoints:
    """Test materials endpoints."""
    
    def test_get_materials_unauthenticated(self, test_client, db_session):
        """Test getting materials without authentication."""
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get("/api/materials")
        
        assert response.status_code == 401
    
    def test_get_materials_empty(self, test_client, db_session):
        """Test getting materials when none exist."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get(
                "/api/materials",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
    
    def test_get_materials_with_data(self, test_client, db_session):
        """Test getting materials with existing data."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material1 = Material(title="Material 1", content="Content 1", category="Python")
        material2 = Material(title="Material 2", content="Content 2", category="JavaScript")
        db_session.add(material1)
        db_session.add(material2)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get(
                "/api/materials",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]["title"] in ["Material 1", "Material 2"]
    
    def test_get_materials_with_search(self, test_client, db_session):
        """Test getting materials with search query."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material1 = Material(title="Python Basics", content="Learn Python", category="Python")
        material2 = Material(title="JavaScript Advanced", content="Advanced JS", category="JavaScript")
        db_session.add(material1)
        db_session.add(material2)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get(
                "/api/materials?search=Python",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert "Python" in data[0]["title"]
    
    def test_get_materials_with_category_filter(self, test_client, db_session):
        """Test getting materials with category filter."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material1 = Material(title="Material 1", content="Content 1", category="Python")
        material2 = Material(title="Material 2", content="Content 2", category="JavaScript")
        db_session.add(material1)
        db_session.add(material2)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get(
                "/api/materials?category=Python",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["category"] == "Python"
    
    def test_get_material_detail(self, test_client, db_session):
        """Test getting a specific material."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(
            title="Test Material",
            content="Test content",
            category="Python"
        )
        db_session.add(material)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get(
                f"/api/materials/{material.id}",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == material.id
        assert data["title"] == "Test Material"
        assert "is_bookmarked" in data
        assert "progress" in data
    
    def test_get_material_not_found(self, test_client, db_session):
        """Test getting a non-existent material."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get(
                "/api/materials/99999",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 404
    
    def test_sync_notion_success(self, test_client, db_session):
        """Test syncing materials from Notion."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        db_session.commit()
        token = create_session(student.id)
        
        # Mock Notion API response
        mock_pages = [
            {
                "id": "page-1",
                "url": "https://notion.so/page-1",
                "properties": {
                    "title": {
                        "title": [{"plain_text": "Notion Page 1"}]
                    }
                }
            }
        ]
        
        async def mock_fetch_pages():
            return mock_pages
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            with patch('backend.main.notion_service.fetch_pages', side_effect=mock_fetch_pages):
                response = test_client.post(
                    "/api/materials/sync-notion",
                    headers={"Cookie": f"session_token={token}"}
                )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["synced"] == 1
    
    def test_get_categories(self, test_client, db_session):
        """Test getting material categories."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material1 = Material(title="M1", content="C1", category="Python")
        material2 = Material(title="M2", content="C2", category="JavaScript")
        material3 = Material(title="M3", content="C3", category="Python")
        db_session.add_all([material1, material2, material3])
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get(
                "/api/materials/categories",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "Python" in data
        assert "JavaScript" in data
        assert len(data) == 2


class TestBookmarksEndpoints:
    """Test bookmarks endpoints."""
    
    def test_get_bookmarks_empty(self, test_client, db_session):
        """Test getting bookmarks when none exist."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get(
                "/api/bookmarks",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
    
    def test_create_bookmark_success(self, test_client, db_session):
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
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.post(
                "/api/bookmarks",
                json={"material_id": material.id},
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["bookmark"]["material_id"] == material.id
    
    def test_create_bookmark_duplicate(self, test_client, db_session):
        """Test creating a duplicate bookmark."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        
        bookmark = Bookmark(student_id=student.id, material_id=material.id)
        db_session.add(bookmark)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.post(
                "/api/bookmarks",
                json={"material_id": material.id},
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_delete_bookmark(self, test_client, db_session):
        """Test deleting a bookmark."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        
        bookmark = Bookmark(student_id=student.id, material_id=material.id)
        db_session.add(bookmark)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.delete(
                f"/api/bookmarks/{bookmark.id}",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        
        # Verify bookmark was deleted
        deleted = db_session.query(Bookmark).filter(Bookmark.id == bookmark.id).first()
        assert deleted is None
    
    def test_delete_bookmark_by_material(self, test_client, db_session):
        """Test deleting a bookmark by material ID."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        
        bookmark = Bookmark(student_id=student.id, material_id=material.id)
        db_session.add(bookmark)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.delete(
                f"/api/bookmarks/material/{material.id}",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True


class TestProgressEndpoints:
    """Test progress endpoints."""
    
    def test_get_progress_empty(self, test_client, db_session):
        """Test getting progress when none exists."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get(
                "/api/progress",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
    
    def test_update_progress_create(self, test_client, db_session):
        """Test creating a new progress record."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.post(
                f"/api/progress/material/{material.id}",
                json={"status": "in_progress", "progress_percentage": 50.0},
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["progress"]["status"] == "in_progress"
        assert data["progress"]["progress_percentage"] == 50.0
    
    def test_update_progress_invalid_status(self, test_client, db_session):
        """Test updating progress with invalid status."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.post(
                f"/api/progress/material/{material.id}",
                json={"status": "invalid_status", "progress_percentage": 50.0},
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_update_progress_invalid_percentage(self, test_client, db_session):
        """Test updating progress with invalid percentage."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.post(
                f"/api/progress/material/{material.id}",
                json={"status": "in_progress", "progress_percentage": 150.0},
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_get_material_progress(self, test_client, db_session):
        """Test getting progress for a specific material."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material = Material(title="Test Material", content="Content")
        db_session.add(material)
        
        progress = Progress(
            student_id=student.id,
            material_id=material.id,
            status="in_progress",
            progress_percentage=75.0
        )
        db_session.add(progress)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get(
                f"/api/progress/material/{material.id}",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "in_progress"
        assert data["progress_percentage"] == 75.0


class TestDashboardEndpoints:
    """Test dashboard endpoints."""
    
    def test_get_dashboard_stats(self, test_client, db_session):
        """Test getting dashboard statistics."""
        student = Student(
            email="test@example.com",
            name="Test User",
            password_hash=hash_password("password123")
        )
        db_session.add(student)
        
        material1 = Material(title="M1", content="C1", category="Python")
        material2 = Material(title="M2", content="C2", category="JavaScript")
        db_session.add_all([material1, material2])
        
        bookmark = Bookmark(student_id=student.id, material_id=material1.id)
        db_session.add(bookmark)
        
        progress = Progress(
            student_id=student.id,
            material_id=material1.id,
            status="completed",
            progress_percentage=100.0
        )
        db_session.add(progress)
        db_session.commit()
        token = create_session(student.id)
        
        with patch('backend.main.SessionLocal', return_value=db_session):
            response = test_client.get(
                "/api/dashboard/stats",
                headers={"Cookie": f"session_token={token}"}
            )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["total_materials"] == 2
        assert data["total_bookmarks"] == 1
        assert data["completed_materials"] == 1
        assert "recent_bookmarks" in data
        assert "recent_progress" in data
