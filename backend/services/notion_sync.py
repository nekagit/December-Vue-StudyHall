"""
Notion sync service for syncing materials from Notion database.
"""
import os
from typing import List, Dict, Any, Optional
import httpx
from backend.models import Material


NOTION_API_KEY = os.getenv('NOTION_API_KEY', '')
DATABASE_ID = os.getenv('NOTION_DATABASE_ID', '')


class NotionSyncService:
    """Service for syncing materials from Notion."""
    
    def __init__(self):
        self.api_key = NOTION_API_KEY
        self.database_id = DATABASE_ID
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        self.client = httpx.AsyncClient()
    
    async def fetch_pages(self) -> List[Dict[str, Any]]:
        """Fetch all pages from the Notion database."""
        if not self.api_key or not self.database_id:
            return []
        
        try:
            url = f'https://api.notion.com/v1/databases/{self.database_id}/query'
            all_pages = []
            has_more = True
            start_cursor = None
            
            while has_more:
                payload = {}
                if start_cursor:
                    payload['start_cursor'] = start_cursor
                
                response = await self.client.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                all_pages.extend(data.get('results', []))
                has_more = data.get('has_more', False)
                start_cursor = data.get('next_cursor')
            
            return all_pages
        except Exception as e:
            print(f"Error fetching pages from Notion: {e}")
            return []
    
    def _extract_title(self, properties: Dict[str, Any]) -> str:
        """Extract title from Notion page properties."""
        # Try common title property names
        for prop_name in ['title', 'Name', 'Title', 'name']:
            if prop_name in properties:
                prop = properties[prop_name]
                if prop.get('type') == 'title' and prop.get('title'):
                    title_parts = [item.get('plain_text', '') for item in prop['title']]
                    title = ''.join(title_parts).strip()
                    if title:
                        return title
        
        # Try to find any title-like property
        for prop_name, prop_value in properties.items():
            if isinstance(prop_value, dict):
                if prop_value.get('type') == 'title' and prop_value.get('title'):
                    title_parts = [item.get('plain_text', '') for item in prop_value['title']]
                    title = ''.join(title_parts).strip()
                    if title:
                        return title
        
        return "Untitled"
    
    def _extract_category(self, properties: Dict[str, Any]) -> Optional[str]:
        """Extract category from Notion page properties."""
        # Try common category property names
        for prop_name in ['category', 'Category', 'Type', 'type', 'Tag', 'tag']:
            if prop_name in properties:
                prop = properties[prop_name]
                prop_type = prop.get('type')
                
                if prop_type == 'select' and prop.get('select'):
                    return prop['select'].get('name')
                elif prop_type == 'multi_select' and prop.get('multi_select'):
                    # Return first category if multiple
                    if prop['multi_select']:
                        return prop['multi_select'][0].get('name')
                elif prop_type == 'rich_text' and prop.get('rich_text'):
                    text_parts = [item.get('plain_text', '') for item in prop['rich_text']]
                    category = ''.join(text_parts).strip()
                    if category:
                        return category
        
        return None
    
    async def _fetch_page_blocks(self, page_id: str) -> List[Dict[str, Any]]:
        """Fetch all blocks for a Notion page."""
        try:
            url = f'https://api.notion.com/v1/blocks/{page_id}/children'
            all_blocks = []
            has_more = True
            start_cursor = None
            
            while has_more:
                params = {}
                if start_cursor:
                    params['start_cursor'] = start_cursor
                
                response = await self.client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()
                
                all_blocks.extend(data.get('results', []))
                has_more = data.get('has_more', False)
                start_cursor = data.get('next_cursor')
            
            return all_blocks
        except Exception as e:
            print(f"Error fetching blocks for page {page_id}: {e}")
            return []
    
    def _block_to_markdown(self, block: Dict[str, Any]) -> str:
        """Convert a Notion block to markdown."""
        block_type = block.get('type', '')
        block_data = block.get(block_type, {})
        
        if block_type == 'paragraph':
            text_parts = []
            for text_item in block_data.get('rich_text', []):
                text = text_item.get('plain_text', '')
                annotations = text_item.get('annotations', {})
                
                # Apply formatting
                if annotations.get('bold'):
                    text = f'**{text}**'
                if annotations.get('italic'):
                    text = f'*{text}*'
                if annotations.get('code'):
                    text = f'`{text}`'
                if annotations.get('strikethrough'):
                    text = f'~~{text}~~'
                
                text_parts.append(text)
            
            return ''.join(text_parts) + '\n\n'
        
        elif block_type == 'heading_1':
            text_parts = [item.get('plain_text', '') for item in block_data.get('rich_text', [])]
            text = ''.join(text_parts)
            return f'# {text}\n\n'
        
        elif block_type == 'heading_2':
            text_parts = [item.get('plain_text', '') for item in block_data.get('rich_text', [])]
            text = ''.join(text_parts)
            return f'## {text}\n\n'
        
        elif block_type == 'heading_3':
            text_parts = [item.get('plain_text', '') for item in block_data.get('rich_text', [])]
            text = ''.join(text_parts)
            return f'### {text}\n\n'
        
        elif block_type == 'bulleted_list_item':
            text_parts = [item.get('plain_text', '') for item in block_data.get('rich_text', [])]
            text = ''.join(text_parts)
            return f'- {text}\n'
        
        elif block_type == 'numbered_list_item':
            text_parts = [item.get('plain_text', '') for item in block_data.get('rich_text', [])]
            text = ''.join(text_parts)
            return f'1. {text}\n'
        
        elif block_type == 'code':
            text_parts = [item.get('plain_text', '') for item in block_data.get('rich_text', [])]
            code = ''.join(text_parts)
            language = block_data.get('language', '')
            return f'```{language}\n{code}\n```\n\n'
        
        elif block_type == 'quote':
            text_parts = [item.get('plain_text', '') for item in block_data.get('rich_text', [])]
            text = ''.join(text_parts)
            return f'> {text}\n\n'
        
        elif block_type == 'divider':
            return '---\n\n'
        
        elif block_type == 'to_do':
            text_parts = [item.get('plain_text', '') for item in block_data.get('rich_text', [])]
            text = ''.join(text_parts)
            checked = 'x' if block_data.get('checked') else ' '
            return f'- [{checked}] {text}\n'
        
        return ''
    
    async def _get_page_content(self, page_id: str) -> str:
        """Fetch and convert page blocks to markdown content."""
        blocks = await self._fetch_page_blocks(page_id)
        markdown_parts = []
        
        for block in blocks:
            markdown = self._block_to_markdown(block)
            if markdown:
                markdown_parts.append(markdown)
        
        return ''.join(markdown_parts).strip()
    
    async def sync_materials(self) -> List[str]:
        """Sync Notion pages and return list of page IDs."""
        pages = await self.fetch_pages()
        page_ids = [page.get('id', '') for page in pages if page.get('id')]
        return page_ids
    
    async def sync_to_database(self, db_session) -> Dict[str, Any]:
        """Sync Notion pages to local database."""
        pages = await self.fetch_pages()
        
        synced_count = 0
        error_count = 0
        
        for page in pages:
            try:
                page_id = page.get('id', '')
                if not page_id:
                    continue
                
                page_url = page.get('url', '')
                properties = page.get('properties', {})
                
                # Extract title and category
                title = self._extract_title(properties)
                category = self._extract_category(properties)
                
                # Fetch page content
                content = await self._get_page_content(page_id)
                
                # Check if material already exists
                existing_material = db_session.query(Material).filter(
                    Material.notion_page_id == page_id
                ).first()
                
                if existing_material:
                    # Update existing material
                    existing_material.title = title
                    existing_material.content = content
                    existing_material.notion_url = page_url
                    if category:
                        existing_material.category = category
                    db_session.commit()
                    # Don't count updates as "synced" (only new materials)
                else:
                    # Create new material
                    new_material = Material(
                        title=title,
                        content=content,
                        notion_page_id=page_id,
                        notion_url=page_url,
                        category=category,
                        order_index=0
                    )
                    db_session.add(new_material)
                    db_session.commit()
                    synced_count += 1
                
            except Exception as e:
                print(f"Error syncing page {page.get('id')}: {e}")
                error_count += 1
                db_session.rollback()
        
        return {
            'success': True,
            'synced': synced_count,
            'errors': error_count,
            'total': len(pages)
        }
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


# Global instance
notion_service = NotionSyncService()





