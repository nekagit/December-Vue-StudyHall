import pytest
from unittest.mock import Mock, AsyncMock, patch
from backend.services.notion_sync import NotionSyncService
import os


class TestNotionSyncService:
    """Tests for Notion sync service."""
    
    @pytest.fixture
    def notion_service(self):
        """Create a NotionSyncService instance."""
        return NotionSyncService()
    
    def test_notion_service_initialization(self, notion_service):
        """Test that NotionSyncService initializes correctly."""
        assert notion_service.client is not None
        assert notion_service.headers is not None
        assert "Authorization" in notion_service.headers
        assert "Content-Type" in notion_service.headers
        assert "Notion-Version" in notion_service.headers
    
    @pytest.mark.asyncio
    async def test_fetch_pages_no_api_key(self, notion_service):
        """Test fetch_pages when API key is missing."""
        with patch.dict(os.environ, {"NOTION_API_KEY": ""}):
            pages = await notion_service.fetch_pages()
            assert pages == []
    
    @pytest.mark.asyncio
    async def test_fetch_pages_success(self):
        """Test successful fetch_pages."""
        # Create a new service instance after patching
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {"id": "page1", "url": "https://notion.so/page1"},
                {"id": "page2", "url": "https://notion.so/page2"}
            ]
        }
        mock_response.raise_for_status = Mock()
        
        # Patch the module-level constants
        with patch('backend.services.notion_sync.NOTION_API_KEY', "test-key"):
            with patch('backend.services.notion_sync.DATABASE_ID', "test-db-id"):
                # Create a new service instance with patched values
                service = NotionSyncService()
                with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
                    mock_post.return_value = mock_response
                    
                    pages = await service.fetch_pages()
                    
                    assert len(pages) == 2
                    assert pages[0]["id"] == "page1"
                    assert pages[1]["id"] == "page2"
                    mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_fetch_pages_error(self, notion_service):
        """Test fetch_pages when API call fails."""
        with patch.dict(os.environ, {"NOTION_API_KEY": "test-key", "NOTION_DATABASE_ID": "test-db-id"}):
            with patch.object(notion_service.client, 'post', new_callable=AsyncMock) as mock_post:
                mock_post.side_effect = Exception("API Error")
                
                pages = await notion_service.fetch_pages()
                
                assert pages == []
    
    @pytest.mark.asyncio
    async def test_fetch_pages_empty_results(self, notion_service):
        """Test fetch_pages when API returns empty results."""
        mock_response = Mock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = Mock()
        
        with patch.dict(os.environ, {"NOTION_API_KEY": "test-key", "NOTION_DATABASE_ID": "test-db-id"}):
            with patch.object(notion_service.client, 'post', new_callable=AsyncMock) as mock_post:
                mock_post.return_value = mock_response
                
                pages = await notion_service.fetch_pages()
                
                assert pages == []
    
    @pytest.mark.asyncio
    async def test_sync_materials(self, notion_service):
        """Test sync_materials method."""
        mock_pages = [
            {"id": "page1", "url": "https://notion.so/page1"},
            {"id": "page2", "url": "https://notion.so/page2"}
        ]
        
        with patch.object(notion_service, 'fetch_pages', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_pages
            
            page_ids = await notion_service.sync_materials()
            
            assert len(page_ids) == 2
            assert "page1" in page_ids
            assert "page2" in page_ids
