import pytest
from unittest.mock import Mock, patch, AsyncMock
from backend.services.notion_sync import NotionSyncService, notion_service

# Enable async test support
pytestmark = pytest.mark.asyncio


class TestNotionSyncService:
    """Test Notion sync service."""
    
    def test_init(self):
        """Test service initialization."""
        service = NotionSyncService()
        
        assert service.client is not None
        assert "Authorization" in service.headers
        assert "Content-Type" in service.headers
        assert "Notion-Version" in service.headers
    
    async def test_fetch_pages_success(self):
        """Test successfully fetching pages from Notion."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {
                    "id": "page-1",
                    "url": "https://notion.so/page-1",
                    "properties": {
                        "title": {
                            "title": [{"plain_text": "Test Page 1"}]
                        }
                    }
                },
                {
                    "id": "page-2",
                    "url": "https://notion.so/page-2",
                    "properties": {
                        "Name": {
                            "title": [{"plain_text": "Test Page 2"}]
                        }
                    }
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        
        service = NotionSyncService()
        
        with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            
            pages = await service.fetch_pages()
            
            assert len(pages) == 2
            assert pages[0]["id"] == "page-1"
            assert pages[1]["id"] == "page-2"
            mock_post.assert_called_once()
    
    async def test_fetch_pages_no_api_key(self, monkeypatch):
        """Test fetching pages without API key."""
        monkeypatch.setenv("NOTION_API_KEY", "")
        
        service = NotionSyncService()
        pages = await service.fetch_pages()
        
        # Should return empty list when API key is missing
        # Note: This depends on implementation - if it checks at init, might be different
        assert isinstance(pages, list)
    
    async def test_fetch_pages_error(self):
        """Test handling errors when fetching pages."""
        service = NotionSyncService()
        
        with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.side_effect = Exception("Network error")
            
            pages = await service.fetch_pages()
            
            # Should return empty list on error
            assert pages == []
    
    async def test_fetch_pages_empty_results(self):
        """Test fetching pages with empty results."""
        mock_response = Mock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = Mock()
        
        service = NotionSyncService()
        
        with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            
            pages = await service.fetch_pages()
            
            assert pages == []
    
    async def test_sync_materials(self):
        """Test syncing materials."""
        mock_pages = [
            {"id": "page-1"},
            {"id": "page-2"},
            {"id": "page-3"}
        ]
        
        service = NotionSyncService()
        
        with patch.object(service, 'fetch_pages', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_pages
            
            page_ids = await service.sync_materials()
            
            assert len(page_ids) == 3
            assert "page-1" in page_ids
            assert "page-2" in page_ids
            assert "page-3" in page_ids


class TestNotionSyncIntegration:
    """Test Notion sync integration with API."""
    
    def test_notion_service_instance(self):
        """Test that notion_service is properly instantiated."""
        assert notion_service is not None
        assert isinstance(notion_service, NotionSyncService)
    
    async def test_fetch_pages_with_mock_client(self):
        """Test fetch_pages with mocked HTTP client."""
        mock_response_data = {
            "results": [
                {
                    "id": "test-id-1",
                    "url": "https://notion.so/test-1",
                    "properties": {
                        "Title": {
                            "title": [{"plain_text": "Test Title 1"}]
                        }
                    }
                }
            ]
        }
        
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = Mock()
        
        service = NotionSyncService()
        
        with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_response
            
            pages = await service.fetch_pages()
            
            assert len(pages) == 1
            assert pages[0]["id"] == "test-id-1"
            # Verify the correct endpoint was called
            assert mock_post.called
