import pytest
from backend.models import Student, Material, Bookmark, Progress
from backend.services.auth import create_student


class TestAuthEndpoints:
    """Test authentication endpoints."""
    
    def test_register_success(self, test_client, db_session):
        """Test successful user registration."""
        response = test_client.post(
            '/api/auth/register',
            json={
                'email': 'newuser@example.com',
                'name': 'New User',
                'password': 'password123'
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['student']['email'] == 'newuser@example.com'
        assert data['student']['name'] == 'New User'
        assert 'session_token' in response.headers.get('Set-Cookie', '')
    
    def test_register_duplicate_email(self, test_client, db_session, sample_student):
        """Test registration with duplicate email."""
        response = test_client.post(
            '/api/auth/register',
            json={
                'email': 'test@example.com',
                'name': 'Another User',
                'password': 'password123'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'already registered' in data['error'].lower()
    
    def test_register_max_students(self, test_client, db_session):
        """Test registration when max students limit is reached."""
        # Create 30 students
        for i in range(30):
            create_student(
                db_session,
                email=f'student{i}@example.com',
                name=f'Student {i}',
                password='password123'
            )
        
        response = test_client.post(
            '/api/auth/register',
            json={
                'email': 'newstudent@example.com',
                'name': 'New Student',
                'password': 'password123'
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert '30' in data['error']
    
    def test_login_success(self, test_client, db_session, sample_student):
        """Test successful login."""
        response = test_client.post(
            '/api/auth/login',
            json={
                'email': 'test@example.com',
                'password': 'testpassword123'
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['student']['email'] == 'test@example.com'
        assert 'session_token' in response.headers.get('Set-Cookie', '')
    
    def test_login_invalid_email(self, test_client, db_session):
        """Test login with invalid email."""
        response = test_client.post(
            '/api/auth/login',
            json={
                'email': 'nonexistent@example.com',
                'password': 'password123'
            }
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
    
    def test_login_invalid_password(self, test_client, db_session, sample_student):
        """Test login with invalid password."""
        response = test_client.post(
            '/api/auth/login',
            json={
                'email': 'test@example.com',
                'password': 'wrongpassword'
            }
        )
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
    
    def test_logout(self, authenticated_client):
        """Test logout."""
        client, _ = authenticated_client
        response = client.post('/api/auth/logout')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_get_current_user_success(self, authenticated_client):
        """Test getting current authenticated user."""
        client, _ = authenticated_client
        response = client.get('/api/auth/me')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'id' in data
        assert 'email' in data
        assert 'name' in data
        assert data['email'] == 'test@example.com'
    
    def test_get_current_user_unauthenticated(self, test_client):
        """Test getting current user without authentication."""
        response = test_client.get('/api/auth/me')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data


class TestMaterialsEndpoints:
    """Test materials endpoints."""
    
    def test_get_materials_empty(self, authenticated_client):
        """Test getting materials when none exist."""
        client, _ = authenticated_client
        response = client.get('/api/materials')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_materials_with_data(self, authenticated_client, db_session, sample_material):
        """Test getting materials with existing data."""
        client, _ = authenticated_client
        
        # Create another material
        material2 = Material(
            title="Another Material",
            content="More content",
            category="JavaScript",
            order_index=2
        )
        db_session.add(material2)
        db_session.commit()
        
        response = client.get('/api/materials')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert any(m['title'] == 'Test Material' for m in data)
        assert any(m['title'] == 'Another Material' for m in data)
    
    def test_get_materials_search(self, authenticated_client, db_session):
        """Test searching materials."""
        client, _ = authenticated_client
        
        # Create materials with different titles
        material1 = Material(title="Python Basics", content="Learn Python", category="Python")
        material2 = Material(title="JavaScript Advanced", content="Advanced JS", category="JavaScript")
        db_session.add_all([material1, material2])
        db_session.commit()
        
        response = client.get('/api/materials?search=Python')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['title'] == 'Python Basics'
    
    def test_get_materials_category_filter(self, authenticated_client, db_session):
        """Test filtering materials by category."""
        client, _ = authenticated_client
        
        material1 = Material(title="Python Basics", content="Learn Python", category="Python")
        material2 = Material(title="JavaScript Basics", content="Learn JS", category="JavaScript")
        db_session.add_all([material1, material2])
        db_session.commit()
        
        response = client.get('/api/materials?category=Python')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['category'] == 'Python'
    
    def test_get_materials_unauthenticated(self, test_client):
        """Test getting materials without authentication."""
        response = test_client.get('/api/materials')
        
        assert response.status_code == 401
    
    def test_get_material_detail(self, authenticated_client, db_session, sample_material):
        """Test getting a specific material."""
        client, _ = authenticated_client
        response = client.get(f'/api/materials/{sample_material.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == sample_material.id
        assert data['title'] == 'Test Material'
        assert data['content'] == 'This is test content'
    
    def test_get_material_not_found(self, authenticated_client):
        """Test getting non-existent material."""
        client, _ = authenticated_client
        response = client.get('/api/materials/99999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
    
    def test_get_materials_with_bookmarks(self, authenticated_client, db_session, sample_student, sample_material):
        """Test materials endpoint includes bookmark status."""
        client, _ = authenticated_client
        
        # Create a bookmark
        bookmark = Bookmark(student_id=sample_student.id, material_id=sample_material.id)
        db_session.add(bookmark)
        db_session.commit()
        
        response = client.get('/api/materials')
        
        assert response.status_code == 200
        data = response.get_json()
        material = next(m for m in data if m['id'] == sample_material.id)
        assert material['is_bookmarked'] is True


class TestBookmarksEndpoints:
    """Test bookmarks endpoints."""
    
    def test_get_bookmarks_empty(self, authenticated_client):
        """Test getting bookmarks when none exist."""
        client, _ = authenticated_client
        response = client.get('/api/bookmarks')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_create_bookmark(self, authenticated_client, db_session, sample_student, sample_material):
        """Test creating a bookmark."""
        client, _ = authenticated_client
        response = client.post(
            '/api/bookmarks',
            json={'material_id': sample_material.id}
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert data['bookmark']['material_id'] == sample_material.id
    
    def test_create_bookmark_duplicate(self, authenticated_client, db_session, sample_student, sample_material):
        """Test creating duplicate bookmark."""
        client, _ = authenticated_client
        
        # Create first bookmark
        bookmark = Bookmark(student_id=sample_student.id, material_id=sample_material.id)
        db_session.add(bookmark)
        db_session.commit()
        
        # Try to create duplicate
        response = client.post(
            '/api/bookmarks',
            json={'material_id': sample_material.id}
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'already exists' in data['error'].lower()
    
    def test_create_bookmark_material_not_found(self, authenticated_client):
        """Test creating bookmark for non-existent material."""
        client, _ = authenticated_client
        response = client.post(
            '/api/bookmarks',
            json={'material_id': 99999}
        )
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
    
    def test_create_bookmark_missing_material_id(self, authenticated_client):
        """Test creating bookmark without material_id."""
        client, _ = authenticated_client
        response = client.post('/api/bookmarks', json={})
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_get_bookmarks_with_data(self, authenticated_client, db_session, sample_student, sample_material):
        """Test getting bookmarks with existing data."""
        client, _ = authenticated_client
        
        bookmark = Bookmark(student_id=sample_student.id, material_id=sample_material.id)
        db_session.add(bookmark)
        db_session.commit()
        
        response = client.get('/api/bookmarks')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['material_id'] == sample_material.id
        assert 'material' in data[0]
    
    def test_delete_bookmark(self, authenticated_client, db_session, sample_student, sample_material):
        """Test deleting a bookmark."""
        client, _ = authenticated_client
        
        bookmark = Bookmark(student_id=sample_student.id, material_id=sample_material.id)
        db_session.add(bookmark)
        db_session.commit()
        
        response = client.delete(f'/api/bookmarks/{bookmark.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_delete_bookmark_not_found(self, authenticated_client):
        """Test deleting non-existent bookmark."""
        client, _ = authenticated_client
        response = client.delete('/api/bookmarks/99999')
        
        assert response.status_code == 404
    
    def test_delete_bookmark_by_material(self, authenticated_client, db_session, sample_student, sample_material):
        """Test deleting bookmark by material ID."""
        client, _ = authenticated_client
        
        bookmark = Bookmark(student_id=sample_student.id, material_id=sample_material.id)
        db_session.add(bookmark)
        db_session.commit()
        
        response = client.delete(f'/api/bookmarks/material/{sample_material.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True


class TestProgressEndpoints:
    """Test progress endpoints."""
    
    def test_get_progress_empty(self, authenticated_client):
        """Test getting progress when none exists."""
        client, _ = authenticated_client
        response = client.get('/api/progress')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_material_progress_not_started(self, authenticated_client, db_session, sample_material):
        """Test getting progress for material that hasn't been started."""
        client, _ = authenticated_client
        response = client.get(f'/api/progress/material/{sample_material.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'not_started'
        assert data['progress_percentage'] == 0.0
    
    def test_update_progress_create(self, authenticated_client, db_session, sample_material):
        """Test creating progress record."""
        client, _ = authenticated_client
        response = client.post(
            f'/api/progress/material/{sample_material.id}',
            json={
                'status': 'in_progress',
                'progress_percentage': 50.0
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['progress']['status'] == 'in_progress'
        assert data['progress']['progress_percentage'] == 50.0
    
    def test_update_progress_update(self, authenticated_client, db_session, sample_student, sample_material):
        """Test updating existing progress record."""
        client, _ = authenticated_client
        
        # Create initial progress
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id,
            status='in_progress',
            progress_percentage=30.0
        )
        db_session.add(progress)
        db_session.commit()
        
        # Update progress
        response = client.put(
            f'/api/progress/material/{sample_material.id}',
            json={
                'status': 'completed',
                'progress_percentage': 100.0
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['progress']['status'] == 'completed'
        assert data['progress']['progress_percentage'] == 100.0
        assert data['progress']['completed_at'] is not None
    
    def test_update_progress_invalid_status(self, authenticated_client, db_session, sample_material):
        """Test updating progress with invalid status."""
        client, _ = authenticated_client
        response = client.post(
            f'/api/progress/material/{sample_material.id}',
            json={
                'status': 'invalid_status',
                'progress_percentage': 50.0
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_update_progress_invalid_percentage(self, authenticated_client, db_session, sample_material):
        """Test updating progress with invalid percentage."""
        client, _ = authenticated_client
        response = client.post(
            f'/api/progress/material/{sample_material.id}',
            json={
                'status': 'in_progress',
                'progress_percentage': 150.0
            }
        )
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_get_progress_with_data(self, authenticated_client, db_session, sample_student, sample_material):
        """Test getting progress with existing data."""
        client, _ = authenticated_client
        
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id,
            status='completed',
            progress_percentage=100.0
        )
        db_session.add(progress)
        db_session.commit()
        
        response = client.get('/api/progress')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['status'] == 'completed'
        assert 'material' in data[0]


class TestDashboardEndpoints:
    """Test dashboard endpoints."""
    
    def test_get_dashboard_stats(self, authenticated_client, db_session, sample_student, sample_material):
        """Test getting dashboard statistics."""
        client, _ = authenticated_client
        
        # Create some test data
        bookmark = Bookmark(student_id=sample_student.id, material_id=sample_material.id)
        progress = Progress(
            student_id=sample_student.id,
            material_id=sample_material.id,
            status='completed',
            progress_percentage=100.0
        )
        db_session.add_all([bookmark, progress])
        db_session.commit()
        
        response = client.get('/api/dashboard/stats')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'total_materials' in data
        assert 'total_bookmarks' in data
        assert 'completed_materials' in data
        assert 'in_progress_materials' in data
        assert 'recent_bookmarks' in data
        assert 'recent_progress' in data
        assert data['total_materials'] >= 1
        assert data['total_bookmarks'] == 1
        assert data['completed_materials'] == 1


class TestCategoriesEndpoint:
    """Test categories endpoint."""
    
    def test_get_categories(self, authenticated_client, db_session):
        """Test getting material categories."""
        client, _ = authenticated_client
        
        # Create materials with different categories
        material1 = Material(title="Python Material", category="Python")
        material2 = Material(title="JS Material", category="JavaScript")
        material3 = Material(title="Python Advanced", category="Python")
        db_session.add_all([material1, material2, material3])
        db_session.commit()
        
        response = client.get('/api/materials/categories')
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert 'Python' in data
        assert 'JavaScript' in data
        assert len(data) == 2  # Should be unique categories
