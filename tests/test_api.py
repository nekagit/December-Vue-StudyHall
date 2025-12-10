import pytest
import json
from backend.models import Student, Material


class TestMaterialsEndpoints:
    """Test materials endpoints."""
    
    def test_get_materials_empty(self, client, db):
        """Test getting materials when none exist."""
        response = client.get("/api/materials")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_materials_single(self, client, db, sample_material):
        """Test getting a single material."""
        response = client.get("/api/materials")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == sample_material.id
        assert data[0]["title"] == sample_material.title
        assert data[0]["content"] == sample_material.content
        assert data[0]["category"] == sample_material.category
    
    def test_get_materials_multiple(self, client, db, multiple_materials):
        """Test getting multiple materials."""
        response = client.get("/api/materials")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 4
        # Verify all materials are returned
        titles = [m["title"] for m in data]
        assert "Python Basics" in titles
        assert "JavaScript Advanced" in titles
    
    def test_get_materials_with_search(self, client, db, multiple_materials):
        """Test getting materials with search query."""
        response = client.get("/api/materials?search=Python")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert all("Python" in m["title"] or "Python" in m["content"] for m in data)
    
    def test_get_materials_with_search_case_insensitive(self, client, db, multiple_materials):
        """Test search is case insensitive."""
        response = client.get("/api/materials?search=python")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
    
    def test_get_materials_with_search_in_content(self, client, db, multiple_materials):
        """Test search matches content as well."""
        response = client.get("/api/materials?search=Learn")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) >= 2
    
    def test_get_materials_with_category(self, client, db, multiple_materials):
        """Test getting materials filtered by category."""
        response = client.get("/api/materials?category=Python")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert all(m["category"] == "Python" for m in data)
    
    def test_get_materials_with_category_and_search(self, client, db, multiple_materials):
        """Test combining category filter and search."""
        response = client.get("/api/materials?category=Python&search=Advanced")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["category"] == "Python"
        assert "Advanced" in data[0]["title"]
    
    def test_get_materials_empty_search(self, client, db, multiple_materials):
        """Test search with empty string returns all."""
        response = client.get("/api/materials?search=")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 4
    
    def test_get_materials_nonexistent_category(self, client, db, multiple_materials):
        """Test filtering by non-existent category."""
        response = client.get("/api/materials?category=Nonexistent")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 0
    
    def test_get_material_detail(self, client, db, sample_material):
        """Test getting a specific material."""
        response = client.get(f"/api/materials/{sample_material.id}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == sample_material.id
        assert data["title"] == sample_material.title
        assert data["content"] == sample_material.content
        assert data["category"] == sample_material.category
        assert "created_at" in data
    
    def test_get_material_not_found(self, client, db):
        """Test getting a non-existent material."""
        response = client.get("/api/materials/99999")
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert "error" in data
    
    def test_get_material_invalid_id(self, client, db):
        """Test getting material with invalid ID."""
        response = client.get("/api/materials/invalid")
        
        assert response.status_code == 404
    
    def test_get_categories(self, client, db, multiple_materials):
        """Test getting all categories."""
        response = client.get("/api/materials/categories")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert "Python" in data
        assert "JavaScript" in data
        assert "Web" in data
        assert len(data) == 3
    
    def test_get_categories_empty(self, client, db):
        """Test getting categories when no materials exist."""
        response = client.get("/api/materials/categories")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_categories_no_duplicates(self, client, db, multiple_materials):
        """Test categories endpoint returns unique values."""
        response = client.get("/api/materials/categories")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == len(set(data))  # No duplicates
    
    def test_get_categories_excludes_none(self, client, db):
        """Test categories endpoint excludes None values."""
        material = Material(title="No Category", content="Test")
        db.add(material)
        db.commit()
        
        response = client.get("/api/materials/categories")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert None not in data


class TestNotionSyncEndpoint:
    """Test Notion sync endpoint."""
    
    def test_sync_notion_no_api_key(self, client, db, monkeypatch):
        """Test syncing when Notion API key is missing."""
        monkeypatch.setenv("NOTION_API_KEY", "")
        
        response = client.post("/api/materials/sync-notion")
        
        # Should handle gracefully
        assert response.status_code in [200, 500]
    
    def test_sync_notion_success(self, client, db, monkeypatch):
        """Test successful Notion sync."""
        from unittest.mock import patch, AsyncMock
        
        mock_pages = [
            {
                "id": "notion-page-1",
                "url": "https://notion.so/test-1",
                "properties": {
                    "title": {
                        "title": [{"plain_text": "Test Page 1"}]
                    }
                }
            },
            {
                "id": "notion-page-2",
                "url": "https://notion.so/test-2",
                "properties": {
                    "Name": {
                        "title": [{"plain_text": "Test Page 2"}]
                    }
                }
            }
        ]
        
        monkeypatch.setenv("NOTION_API_KEY", "test-key")
        monkeypatch.setenv("NOTION_DATABASE_ID", "test-db-id")
        
        with patch('backend.services.notion_sync.notion_service.fetch_pages', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_pages
            
            response = client.post("/api/materials/sync-notion")
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
            assert data["synced"] == 2
    
    def test_sync_notion_duplicate_pages(self, client, db, monkeypatch):
        """Test syncing duplicate pages doesn't create duplicates."""
        from unittest.mock import patch, AsyncMock
        
        # Create existing material
        existing = Material(
            title="Existing",
            notion_page_id="notion-page-1",
            notion_url="https://notion.so/test-1"
        )
        db.add(existing)
        db.commit()
        
        mock_pages = [
            {
                "id": "notion-page-1",
                "url": "https://notion.so/test-1",
                "properties": {
                    "title": {
                        "title": [{"plain_text": "Updated Title"}]
                    }
                }
            },
            {
                "id": "notion-page-2",
                "url": "https://notion.so/test-2",
                "properties": {
                    "Name": {
                        "title": [{"plain_text": "New Page"}]
                    }
                }
            }
        ]
        
        monkeypatch.setenv("NOTION_API_KEY", "test-key")
        monkeypatch.setenv("NOTION_DATABASE_ID", "test-db-id")
        
        with patch('backend.services.notion_sync.notion_service.fetch_pages', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_pages
            
            response = client.post("/api/materials/sync-notion")
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
            assert data["synced"] == 1  # Only new page synced
    
    def test_sync_notion_empty_pages(self, client, db, monkeypatch):
        """Test syncing when no pages returned."""
        from unittest.mock import patch, AsyncMock
        
        monkeypatch.setenv("NOTION_API_KEY", "test-key")
        monkeypatch.setenv("NOTION_DATABASE_ID", "test-db-id")
        
        with patch('backend.services.notion_sync.notion_service.fetch_pages', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = []
            
            response = client.post("/api/materials/sync-notion")
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
            assert data["synced"] == 0
    
    def test_sync_notion_untitled_pages(self, client, db, monkeypatch):
        """Test syncing pages without title property."""
        from unittest.mock import patch, AsyncMock
        
        mock_pages = [
            {
                "id": "notion-page-1",
                "url": "https://notion.so/test-1",
                "properties": {}  # No title property
            }
        ]
        
        monkeypatch.setenv("NOTION_API_KEY", "test-key")
        monkeypatch.setenv("NOTION_DATABASE_ID", "test-db-id")
        
        with patch('backend.services.notion_sync.notion_service.fetch_pages', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_pages
            
            response = client.post("/api/materials/sync-notion")
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
            assert data["synced"] == 1
            
            # Check material was created with "Untitled"
            material = db.query(Material).filter(Material.notion_page_id == "notion-page-1").first()
            assert material is not None
            assert material.title == "Untitled"


class TestExportEndpoint:
    """Test export endpoint."""
    
    def test_export_with_data(self, client):
        """Test exporting work with data."""
        export_data = {
            "date": "2024-01-01",
            "timestamp": "2024-01-01T00:00:00Z",
            "materials_viewed": ["Material 1", "Material 2"],
            "code_executed": ["print('hello')"],
            "notes": ["Note 1"]
        }
        
        response = client.post(
            "/api/export",
            json=export_data,
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["filename"] == "studyhall-export-2024-01-01.json"
        assert data["data"] == export_data
    
    def test_export_empty_data(self, client):
        """Test exporting with empty data."""
        export_data = {
            "date": "2024-01-01",
            "materials_viewed": [],
            "code_executed": [],
            "notes": []
        }
        
        response = client.post(
            "/api/export",
            json=export_data,
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
    
    def test_export_no_data(self, client):
        """Test exporting without data."""
        response = client.post(
            "/api/export",
            data="",
            content_type="application/json"
        )
        
        # Flask returns 400 for bad JSON, but our handler catches it and returns 500
        assert response.status_code in [400, 500]
    
    def test_export_missing_date(self, client):
        """Test exporting with missing date field."""
        export_data = {
            "materials_viewed": ["Material 1"]
        }
        
        response = client.post(
            "/api/export",
            json=export_data,
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert "today" in data["filename"]  # Defaults to "today"
    
    def test_export_large_data(self, client):
        """Test exporting with large amounts of data."""
        export_data = {
            "date": "2024-01-01",
            "materials_viewed": [f"Material {i}" for i in range(100)],
            "code_executed": [f"code_{i}" for i in range(100)],
            "notes": [f"note_{i}" for i in range(100)]
        }
        
        response = client.post(
            "/api/export",
            json=export_data,
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert len(data["data"]["materials_viewed"]) == 100
    
    def test_export_invalid_json(self, client):
        """Test exporting with invalid JSON."""
        response = client.post(
            "/api/export",
            data="not json",
            content_type="application/json"
        )
        
        # Should handle gracefully
        assert response.status_code in [400, 500]
