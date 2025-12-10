import pytest
import json
from unittest.mock import patch, AsyncMock
from backend.models.student import Student
from backend.models.material import Material
from backend.services.auth import hash_password, create_student
from backend.services.session import create_session, _sessions


class TestAuthEndpoints:
    """Tests for authentication endpoints."""
    
    def test_login_success(self, client, api_db_session, sample_student_data):
        """Test successful login."""
        # Create a student
        student = Student(
            email=sample_student_data["email"],
            name=sample_student_data["name"],
            password_hash=hash_password(sample_student_data["password"])
        )
        api_db_session.add(student)
        api_db_session.commit()
        
        # Login
        response = client.post(
            "/api/auth/login",
            json={
                "email": sample_student_data["email"],
                "password": sample_student_data["password"]
            }
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["student"]["email"] == sample_student_data["email"]
        assert data["student"]["name"] == sample_student_data["name"]
        assert "session_token" in response.headers.get("Set-Cookie", "")
    
    def test_login_invalid_credentials(self, client, api_db_session, sample_student_data):
        """Test login with invalid credentials."""
        # Create a student
        student = Student(
            email=sample_student_data["email"],
            name=sample_student_data["name"],
            password_hash=hash_password(sample_student_data["password"])
        )
        api_db_session.add(student)
        api_db_session.commit()
        
        # Try to login with wrong password
        response = client.post(
            "/api/auth/login",
            json={
                "email": sample_student_data["email"],
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
        data = json.loads(response.data)
        assert "error" in data
    
    def test_register_success(self, client, api_db_session, sample_student_data):
        """Test successful registration."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": sample_student_data["email"],
                "name": sample_student_data["name"],
                "password": sample_student_data["password"]
            }
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["student"]["email"] == sample_student_data["email"]
        assert data["student"]["name"] == sample_student_data["name"]
        
        # Verify student was created in database
        student = api_db_session.query(Student).filter(
            Student.email == sample_student_data["email"]
        ).first()
        assert student is not None
    
    def test_register_duplicate_email(self, client, api_db_session, sample_student_data):
        """Test registration with duplicate email."""
        # Create first student
        create_student(
            api_db_session,
            sample_student_data["email"],
            sample_student_data["name"],
            sample_student_data["password"]
        )
        
        # Try to register again with same email
        response = client.post(
            "/api/auth/register",
            json={
                "email": sample_student_data["email"],
                "name": "Another Name",
                "password": "anotherpassword"
            }
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_logout(self, client, api_db_session, sample_student_data):
        """Test logout."""
        # Create student and session
        student = create_student(
            api_db_session,
            sample_student_data["email"],
            sample_student_data["name"],
            sample_student_data["password"]
        )
        token = create_session(student.id)
        
        # Logout
        client.set_cookie("session_token", token)
        response = client.post("/api/auth/logout")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert token not in _sessions
    
    def test_get_current_user_authenticated(self, client, api_db_session, sample_student_data):
        """Test getting current user when authenticated."""
        student = create_student(
            api_db_session,
            sample_student_data["email"],
            sample_student_data["name"],
            sample_student_data["password"]
        )
        token = create_session(student.id)
        
        client.set_cookie("session_token", token)
        response = client.get("/api/auth/me")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == student.id
        assert data["email"] == sample_student_data["email"]
        assert data["name"] == sample_student_data["name"]
    
    def test_get_current_user_unauthenticated(self, client):
        """Test getting current user when not authenticated."""
        response = client.get("/api/auth/me")
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data


class TestMaterialsEndpoints:
    """Tests for materials endpoints."""
    
    def test_get_materials_authenticated(self, client, api_db_session, sample_student_data, sample_material_data):
        """Test getting materials when authenticated."""
        # Create student and session
        student = create_student(
            api_db_session,
            sample_student_data["email"],
            sample_student_data["name"],
            sample_student_data["password"]
        )
        token = create_session(student.id)
        
        # Create materials
        material1 = Material(
            title=sample_material_data["title"],
            content=sample_material_data["content"],
            category=sample_material_data["category"]
        )
        material2 = Material(
            title="Another Material",
            content="Another content",
            category="JavaScript"
        )
        api_db_session.add(material1)
        api_db_session.add(material2)
        api_db_session.commit()
        
        client.set_cookie("session_token", token)
        response = client.get("/api/materials")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data[0]["title"] in [sample_material_data["title"], "Another Material"]
        assert data[1]["title"] in [sample_material_data["title"], "Another Material"]
    
    def test_get_materials_unauthenticated(self, client):
        """Test getting materials when not authenticated."""
        response = client.get("/api/materials")
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
    
    def test_get_materials_empty(self, client, api_db_session, sample_student_data):
        """Test getting materials when none exist."""
        student = create_student(
            api_db_session,
            sample_student_data["email"],
            sample_student_data["name"],
            sample_student_data["password"]
        )
        token = create_session(student.id)
        
        client.set_cookie("session_token", token)
        response = client.get("/api/materials")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []
    
    def test_get_material_by_id_success(self, client, api_db_session, sample_student_data, sample_material_data):
        """Test getting a specific material by ID."""
        student = create_student(
            api_db_session,
            sample_student_data["email"],
            sample_student_data["name"],
            sample_student_data["password"]
        )
        token = create_session(student.id)
        
        material = Material(
            title=sample_material_data["title"],
            content=sample_material_data["content"],
            category=sample_material_data["category"],
            notion_url=sample_material_data["notion_url"]
        )
        api_db_session.add(material)
        api_db_session.commit()
        
        client.set_cookie("session_token", token)
        response = client.get(f"/api/materials/{material.id}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == material.id
        assert data["title"] == sample_material_data["title"]
        assert data["content"] == sample_material_data["content"]
        assert data["category"] == sample_material_data["category"]
    
    def test_get_material_by_id_not_found(self, client, api_db_session, sample_student_data):
        """Test getting a non-existent material."""
        student = create_student(
            api_db_session,
            sample_student_data["email"],
            sample_student_data["name"],
            sample_student_data["password"]
        )
        token = create_session(student.id)
        
        client.set_cookie("session_token", token)
        response = client.get("/api/materials/99999")
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data
    
    def test_get_material_unauthenticated(self, client, api_db_session, sample_material_data):
        """Test getting material when not authenticated."""
        material = Material(
            title=sample_material_data["title"],
            content=sample_material_data["content"]
        )
        api_db_session.add(material)
        api_db_session.commit()
        
        response = client.get(f"/api/materials/{material.id}")
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data


class TestNotionSyncEndpoint:
    """Tests for Notion sync endpoint."""
    
    def test_sync_notion_authenticated(self, client, api_db_session, sample_student_data):
        """Test syncing from Notion when authenticated."""
        student = create_student(
            api_db_session,
            sample_student_data["email"],
            sample_student_data["name"],
            sample_student_data["password"]
        )
        token = create_session(student.id)
        
        # Mock Notion API response
        mock_pages = [
            {
                "id": "page-123",
                "url": "https://notion.so/page-123",
                "properties": {
                    "title": {
                        "title": [{"plain_text": "Test Page"}]
                    }
                }
            }
        ]
        
        client.set_cookie("session_token", token)
        
        with patch("backend.main.notion_service.fetch_pages", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_pages
            
            response = client.post("/api/materials/sync-notion")
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
            assert data["synced"] == 1
            
            # Verify material was created
            material = api_db_session.query(Material).filter(
                Material.notion_page_id == "page-123"
            ).first()
            assert material is not None
            assert material.title == "Test Page"
    
    def test_sync_notion_unauthenticated(self, client):
        """Test syncing from Notion when not authenticated."""
        response = client.post("/api/materials/sync-notion")
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert "error" in data
    
    def test_sync_notion_duplicate_pages(self, client, api_db_session, sample_student_data):
        """Test syncing when pages already exist."""
        student = create_student(
            api_db_session,
            sample_student_data["email"],
            sample_student_data["name"],
            sample_student_data["password"]
        )
        token = create_session(student.id)
        
        # Create existing material
        existing_material = Material(
            title="Existing Material",
            notion_page_id="page-123",
            notion_url="https://notion.so/page-123"
        )
        api_db_session.add(existing_material)
        api_db_session.commit()
        
        mock_pages = [
            {
                "id": "page-123",
                "url": "https://notion.so/page-123",
                "properties": {
                    "title": {
                        "title": [{"plain_text": "Updated Title"}]
                    }
                }
            }
        ]
        
        client.set_cookie("session_token", token)
        
        with patch("backend.main.notion_service.fetch_pages", new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_pages
            
            response = client.post("/api/materials/sync-notion")
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
            assert data["synced"] == 0  # Should not sync duplicate
