from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback

from backend.database import engine, SessionLocal, Base
from backend.models import Material
from backend.services.notion_sync import notion_service

# Create database tables
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# CORS configuration - more permissive for development
CORS(app, 
     supports_credentials=True, 
     origins=["http://localhost:5173", "http://localhost:5000", "http://127.0.0.1:5173"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     expose_headers=["Content-Type"])

# Add explicit OPTIONS handler for all routes
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Credentials", "true")
        return response

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route("/api/materials", methods=["GET"])
def get_materials():
    """Get all materials - no authentication required"""
    db = SessionLocal()
    try:
        query = db.query(Material)
        
        # Search functionality
        search = request.args.get("search", "").strip()
        if search:
            query = query.filter(
                (Material.title.ilike(f"%{search}%")) |
                (Material.content.ilike(f"%{search}%"))
            )
        
        # Category filter
        category = request.args.get("category", "").strip()
        if category:
            query = query.filter(Material.category == category)
        
        materials = query.order_by(Material.order_index, Material.created_at).all()
        
        return jsonify([{
            "id": m.id,
            "title": m.title,
            "content": m.content,
            "category": m.category,
            "notion_url": m.notion_url,
            "created_at": m.created_at.isoformat() if m.created_at else None
        } for m in materials])
    finally:
        db.close()

@app.route("/api/materials/<int:material_id>", methods=["GET"])
def get_material(material_id):
    """Get a specific material - no authentication required"""
    db = SessionLocal()
    try:
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            return jsonify({"error": "Material not found"}), 404
        
        return jsonify({
            "id": material.id,
            "title": material.title,
            "content": material.content,
            "category": material.category,
            "notion_url": material.notion_url,
            "created_at": material.created_at.isoformat() if material.created_at else None
        })
    finally:
        db.close()

@app.route("/api/materials/sync-notion", methods=["POST"])
def sync_notion():
    """Sync materials from Notion - no authentication required"""
    db = SessionLocal()
    try:
        import asyncio
        pages = asyncio.run(notion_service.fetch_pages())
        synced_count = 0
        
        for page in pages:
            title = "Untitled"
            if "properties" in page:
                props = page["properties"]
                for prop_name in ["title", "Name", "Title"]:
                    if prop_name in props:
                        title_prop = props[prop_name]
                        if "title" in title_prop and len(title_prop["title"]) > 0:
                            title = title_prop["title"][0]["plain_text"]
                            break
            
            notion_page_id = page.get("id")
            notion_url = page.get("url", "")
            
            existing = db.query(Material).filter(Material.notion_page_id == notion_page_id).first()
            if not existing:
                material = Material(
                    title=title,
                    notion_page_id=notion_page_id,
                    notion_url=notion_url,
                    content=f"Synced from Notion. Page ID: {notion_page_id}"
                )
                db.add(material)
                synced_count += 1
        
        db.commit()
        return jsonify({"success": True, "synced": synced_count})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Categories endpoint
@app.route("/api/materials/categories", methods=["GET"])
def get_categories():
    """Get all material categories - no authentication required"""
    db = SessionLocal()
    try:
        from sqlalchemy import distinct
        categories = db.query(distinct(Material.category)).filter(Material.category.isnot(None)).all()
        return jsonify([cat[0] for cat in categories if cat[0]])
    finally:
        db.close()

# Export endpoint - allows users to export their work
@app.route("/api/export", methods=["POST"])
def export_work():
    """Export user's work for the day - accepts any data and returns it as downloadable content"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Return the data as JSON that can be downloaded
        # Frontend will handle the actual download
        return jsonify({
            "success": True,
            "data": data,
            "filename": f"studyhall-export-{data.get('date', 'today')}.json"
        })
    except Exception as e:
        app.logger.error(f"Export error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
