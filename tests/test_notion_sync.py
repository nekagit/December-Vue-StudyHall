import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from backend.services.notion_sync import NotionSyncService, notion_service


class TestNotionSyncService:
    """Test Notion sync service."""
    
    def test_init(self):
        """Test service initialization."""
        service = NotionSyncService()
        
        assert service.headers is not None
        assert "Authorization" in service.headers
        assert "Content-Type" in service.headers
        assert "Notion-Version" in service.headers
        assert service.client is not None
    
    @pytest.mark.asyncio
    async def test_fetch_pages_success(self):
        """Test successfully fetching pages from Notion."""
        mock_pages = [
            {
                "id": "page-1",
                "url": "https://notion.so/page-1",
                "properties": {}
            },
            {
                "id": "page-2",
                "url": "https://notion.so/page-2",
                "properties": {}
            }
        ]
        
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": mock_pages}
        mock_response.raise_for_status = MagicMock()
        
        service = NotionSyncService()
        
        with patch('backend.services.notion_sync.NOTION_API_KEY', 'test-key'):
            with patch('backend.services.notion_sync.DATABASE_ID', 'test-db-id'):
                with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
                    mock_post.return_value = mock_response
                    
                    pages = await service.fetch_pages()
                    
                    assert len(pages) == 2
                    assert pages[0]["id"] == "page-1"
                    assert pages[1]["id"] == "page-2"
                    mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_fetch_pages_no_api_key(self):
        """Test fetching pages when API key is missing."""
        service = NotionSyncService()
        
        with patch('backend.services.notion_sync.NOTION_API_KEY', ''):
            pages = await service.fetch_pages()
            
            assert pages == []
    
    @pytest.mark.asyncio
    async def test_fetch_pages_api_error(self):
        """Test handling API errors."""
        service = NotionSyncService()
        
        with patch('backend.services.notion_sync.NOTION_API_KEY', 'test-key'):
            with patch('backend.services.notion_sync.DATABASE_ID', 'test-db-id'):
                with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
                    mock_post.side_effect = Exception("API Error")
                    
                    pages = await service.fetch_pages()
                    
                    assert pages == []
    
    @pytest.mark.asyncio
    async def test_fetch_pages_empty_results(self):
        """Test fetching pages when no results are returned."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = MagicMock()
        
        service = NotionSyncService()
        
        with patch('backend.services.notion_sync.NOTION_API_KEY', 'test-key'):
            with patch('backend.services.notion_sync.DATABASE_ID', 'test-db-id'):
                with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
                    mock_post.return_value = mock_response
                    
                    pages = await service.fetch_pages()
                    
                    assert pages == []
    
    @pytest.mark.asyncio
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
            
            result = await service.sync_materials()
            
            assert len(result) == 3
            assert "page-1" in result
            assert "page-2" in result
            assert "page-3" in result
    
    def test_notion_service_instance(self):
        """Test that notion_service is an instance of NotionSyncService."""
        assert isinstance(notion_service, NotionSyncService)
