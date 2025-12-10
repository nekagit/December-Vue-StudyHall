import pytest
import os
from unittest.mock import Mock, patch, AsyncMock
from backend.services.notion_sync import NotionSyncService, notion_service


class TestNotionSyncService:
    """Test NotionSyncService."""
    
    def test_init(self):
        """Test service initialization."""
        service = NotionSyncService()
        
        assert service.client is not None
        assert 'Authorization' in service.headers
        assert 'Content-Type' in service.headers
        assert 'Notion-Version' in service.headers
    
    @pytest.mark.asyncio
    async def test_fetch_pages_success(self):
        """Test successful page fetching."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {
                    "id": "page_1",
                    "url": "https://notion.so/page1",
                    "properties": {
                        "title": {
                            "title": [{"plain_text": "Page 1"}]
                        }
                    }
                },
                {
                    "id": "page_2",
                    "url": "https://notion.so/page2",
                    "properties": {
                        "Name": {
                            "title": [{"plain_text": "Page 2"}]
                        }
                    }
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        
        service = NotionSyncService()
        
        with patch.dict(os.environ, {'NOTION_API_KEY': 'test_key', 'NOTION_DATABASE_ID': 'test_db'}):
            with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
                mock_post.return_value = mock_response
                
                pages = await service.fetch_pages()
                
                assert len(pages) == 2
                assert pages[0]['id'] == 'page_1'
                assert pages[1]['id'] == 'page_2'
                mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_fetch_pages_no_api_key(self):
        """Test fetching pages without API key."""
        with patch.dict(os.environ, {'NOTION_API_KEY': '', 'NOTION_DATABASE_ID': 'test_db'}, clear=False):
            service = NotionSyncService()
            pages = await service.fetch_pages()
            
            assert pages == []
    
    @pytest.mark.asyncio
    async def test_fetch_pages_empty_results(self):
        """Test fetching pages with empty results."""
        mock_response = Mock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = Mock()
        
        service = NotionSyncService()
        
        with patch.dict(os.environ, {'NOTION_API_KEY': 'test_key', 'NOTION_DATABASE_ID': 'test_db'}):
            with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
                mock_post.return_value = mock_response
                
                pages = await service.fetch_pages()
                
                assert pages == []
    
    @pytest.mark.asyncio
    async def test_fetch_pages_error(self):
        """Test error handling when fetching pages."""
        service = NotionSyncService()
        
        with patch.dict(os.environ, {'NOTION_API_KEY': 'test_key', 'NOTION_DATABASE_ID': 'test_db'}):
            with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
                mock_post.side_effect = Exception("API Error")
                
                pages = await service.fetch_pages()
                
                assert pages == []
    
    @pytest.mark.asyncio
    async def test_fetch_pages_http_error(self):
        """Test HTTP error handling."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("HTTP 401")
        
        service = NotionSyncService()
        
        with patch.dict(os.environ, {'NOTION_API_KEY': 'test_key', 'NOTION_DATABASE_ID': 'test_db'}):
            with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
                mock_post.return_value = mock_response
                
                pages = await service.fetch_pages()
                
                assert pages == []
    
    @pytest.mark.asyncio
    async def test_sync_materials(self):
        """Test syncing materials."""
        mock_pages = [
            {"id": "page_1"},
            {"id": "page_2"},
            {"id": "page_3"}
        ]
        
        service = NotionSyncService()
        
        with patch.object(service, 'fetch_pages', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = mock_pages
            
            page_ids = await service.sync_materials()
            
            assert len(page_ids) == 3
            assert 'page_1' in page_ids
            assert 'page_2' in page_ids
            assert 'page_3' in page_ids
    
    @pytest.mark.asyncio
    async def test_sync_materials_empty(self):
        """Test syncing with no materials."""
        service = NotionSyncService()
        
        with patch.object(service, 'fetch_pages', new_callable=AsyncMock) as mock_fetch:
            mock_fetch.return_value = []
            
            page_ids = await service.sync_materials()
            
            assert page_ids == []


class TestNotionServiceIntegration:
    """Integration tests for notion service."""
    
    def test_notion_service_instance(self):
        """Test that notion_service is an instance of NotionSyncService."""
        assert isinstance(notion_service, NotionSyncService)
    
    @pytest.mark.asyncio
    async def test_fetch_pages_with_different_property_names(self):
        """Test fetching pages with different title property names."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {
                    "id": "page_1",
                    "properties": {
                        "Title": {
                            "title": [{"plain_text": "Title Property"}]
                        }
                    }
                },
                {
                    "id": "page_2",
                    "properties": {
                        "Name": {
                            "title": [{"plain_text": "Name Property"}]
                        }
                    }
                },
                {
                    "id": "page_3",
                    "properties": {
                        "title": {
                            "title": [{"plain_text": "Lowercase Title"}]
                        }
                    }
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        
        service = NotionSyncService()
        
        with patch.dict(os.environ, {'NOTION_API_KEY': 'test_key', 'NOTION_DATABASE_ID': 'test_db'}):
            with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
                mock_post.return_value = mock_response
                
                pages = await service.fetch_pages()
                
                assert len(pages) == 3
                # All pages should be returned regardless of property name
                assert all('id' in page for page in pages)
    
    @pytest.mark.asyncio
    async def test_fetch_pages_missing_properties(self):
        """Test fetching pages with missing properties."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [
                {
                    "id": "page_1",
                    "url": "https://notion.so/page1"
                    # Missing properties
                },
                {
                    "id": "page_2",
                    "properties": {}
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        
        service = NotionSyncService()
        
        with patch.dict(os.environ, {'NOTION_API_KEY': 'test_key', 'NOTION_DATABASE_ID': 'test_db'}):
            with patch.object(service.client, 'post', new_callable=AsyncMock) as mock_post:
                mock_post.return_value = mock_response
                
                pages = await service.fetch_pages()
                
                assert len(pages) == 2
                # Pages should still be returned even without properties
