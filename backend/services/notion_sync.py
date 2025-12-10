import httpx
import os

NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")

class NotionSyncService:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.client = httpx.AsyncClient(base_url="https://api.notion.com/v1", headers=self.headers)

    async def fetch_pages(self):
        if not NOTION_API_KEY:
            print("Notion API Key missing. Skipping sync.")
            return []
        
        try:
            # This is a query to a database. If pages are standalone, use search.
            response = await self.client.post(f"/databases/{DATABASE_ID}/query")
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except Exception as e:
            print(f"Error fetching from Notion: {e}")
            return []

    async def sync_materials(self):
        pages = await self.fetch_pages()
        print(f"Found {len(pages)} pages to sync.")
        # Here we would process blocks and save to local DB
        # For now, just return titles
        return [page.get("id") for page in pages]

notion_service = NotionSyncService()


