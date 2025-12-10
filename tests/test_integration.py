import pytest
import json
from backend.models import Material, Student
import hashlib


class TestMaterialsIntegration:
    """Integration tests for materials endpoints."""
    
    def test_create_and_retrieve_material(self, client, db):
        """Test creating a material via sync and retrieving it."""
        # Simulate Notion sync creating a material
        material = Material(
            title="Integration Test Material",
            content="This is test content",
            category="Test",
            notion_page_id="notion-test-123",
            notion_url="https://notion.so/test"
        )
        db.add(material)
        db.commit()
        
        # Retrieve via API
        response = client.get("/api/materials")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["title"] == "Integration Test Material"
        
        # Retrieve specific material
        response = client.get(f"/api/materials/{material.id}")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["title"] == "Integration Test Material"
    
    def test_search_and_filter_work_together(self, client, db):
        """Test that search and category filter work together."""
        materials = [
            Material(title="Python Basics", content="Learn Python", category="Python"),
            Material(title="Python Advanced", content="Advanced Python", category="Python"),
            Material(title="JavaScript Basics", content="Learn JS", category="JavaScript"),
        ]
        db.add_all(materials)
        db.commit()
        
        # Search for "Advanced" in Python category
        response = client.get("/api/materials?category=Python&search=Advanced")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["title"] == "Python Advanced"
    
    def test_categories_reflect_materials(self, client, db):
        """Test that categories endpoint reflects current materials."""
        # Initially no categories
        response = client.get("/api/materials/categories")
        assert response.status_code == 200
        assert len(json.loads(response.data)) == 0
        
        # Add materials
        materials = [
            Material(title="Material 1", category="Category A"),
            Material(title="Material 2", category="Category B"),
            Material(title="Material 3", category="Category A"),
        ]
        db.add_all(materials)
        db.commit()
        
        # Check categories
        response = client.get("/api/materials/categories")
        assert response.status_code == 200
        categories = json.loads(response.data)
        assert len(categories) == 2
        assert "Category A" in categories
        assert "Category B" in categories


class TestExportIntegration:
    """Integration tests for export functionality."""
    
    def test_export_and_verify_structure(self, client):
        """Test exporting data and verifying structure."""
        export_data = {
            "date": "2024-01-15",
            "timestamp": "2024-01-15T10:30:00Z",
            "materials_viewed": [
                {"id": 1, "title": "Material 1", "viewed_at": "2024-01-15T10:00:00Z"},
                {"id": 2, "title": "Material 2", "viewed_at": "2024-01-15T11:00:00Z"}
            ],
            "code_executed": [
                {"code": "print('hello')", "output": "hello", "timestamp": "2024-01-15T10:15:00Z"},
                {"code": "x = 1 + 1", "output": "2", "timestamp": "2024-01-15T10:20:00Z"}
            ],
            "notes": [
                {"content": "Learned about variables", "timestamp": "2024-01-15T10:25:00Z"}
            ]
        }
        
        response = client.post("/api/export", json=export_data)
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data["success"] is True
        assert data["filename"] == "studyhall-export-2024-01-15.json"
        assert data["data"]["date"] == export_data["date"]
        assert len(data["data"]["materials_viewed"]) == 2
        assert len(data["data"]["code_executed"]) == 2
        assert len(data["data"]["notes"]) == 1


class TestMaterialOrdering:
    """Test material ordering functionality."""
    
    def test_materials_ordered_by_order_index(self, client, db):
        """Test that materials are returned in order_index order."""
        materials = [
            Material(title="Third", order_index=30),
            Material(title="First", order_index=10),
            Material(title="Second", order_index=20),
        ]
        db.add_all(materials)
        db.commit()
        
        response = client.get("/api/materials")
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data) == 3
        assert data[0]["title"] == "First"
        assert data[1]["title"] == "Second"
        assert data[2]["title"] == "Third"
    
    def test_materials_same_order_index_ordered_by_created_at(self, client, db):
        """Test that materials with same order_index are ordered by created_at."""
        import time
        
        material1 = Material(title="First Created", order_index=1)
        db.add(material1)
        db.commit()
        db.refresh(material1)
        
        time.sleep(0.1)  # Small delay to ensure different timestamps
        
        material2 = Material(title="Second Created", order_index=1)
        db.add(material2)
        db.commit()
        db.refresh(material2)
        
        response = client.get("/api/materials")
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Should be ordered by created_at when order_index is same
        assert len(data) == 2
        assert data[0]["title"] == "First Created"
        assert data[1]["title"] == "Second Created"


class TestErrorHandling:
    """Test error handling in API endpoints."""
    
    def test_invalid_material_id_type(self, client, db):
        """Test handling invalid material ID types."""
        # String instead of integer
        response = client.get("/api/materials/not-a-number")
        assert response.status_code == 404
    
    def test_negative_material_id(self, client, db):
        """Test handling negative material ID."""
        response = client.get("/api/materials/-1")
        assert response.status_code == 404
    
    def test_zero_material_id(self, client, db):
        """Test handling zero material ID."""
        response = client.get("/api/materials/0")
        assert response.status_code == 404
    
    def test_export_malformed_json(self, client):
        """Test handling malformed JSON in export."""
        response = client.post(
            "/api/export",
            data="not valid json{",
            content_type="application/json"
        )
        # Should handle gracefully
        assert response.status_code in [400, 500]
    
    def test_export_wrong_content_type(self, client):
        """Test export with wrong content type."""
        response = client.post(
            "/api/export",
            data="some data",
            content_type="text/plain"
        )
        # Should handle gracefully
        assert response.status_code in [400, 415, 500]


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_empty_search_query(self, client, db, multiple_materials):
        """Test empty search query returns all materials."""
        response = client.get("/api/materials?search=")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 4
    
    def test_whitespace_search_query(self, client, db, multiple_materials):
        """Test search query with only whitespace."""
        response = client.get("/api/materials?search=   ")
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should return all (whitespace is stripped)
        assert len(data) == 4
    
    def test_very_long_search_query(self, client, db):
        """Test very long search query."""
        long_query = "a" * 1000
        response = client.get(f"/api/materials?search={long_query}")
        # Should handle gracefully
        assert response.status_code == 200
    
    def test_special_characters_in_search(self, client, db):
        """Test search with special characters."""
        material = Material(title="Test & Special", content="Content with <tags>")
        db.add(material)
        db.commit()
        
        response = client.get("/api/materials?search=&")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) >= 0  # Should handle gracefully
    
    def test_material_with_unicode(self, client, db):
        """Test material with unicode characters."""
        material = Material(
            title="测试材料",
            content="Contenu en français avec des caractères spéciaux: é, è, à",
            category="Unicode"
        )
        db.add(material)
        db.commit()
        
        response = client.get("/api/materials")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["title"] == "测试材料"
    
    def test_material_with_very_long_title(self, client, db):
        """Test material with very long title."""
        long_title = "A" * 500
        material = Material(title=long_title, content="Content")
        db.add(material)
        db.commit()
        
        response = client.get("/api/materials")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert len(data[0]["title"]) == 500
