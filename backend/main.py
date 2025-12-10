from flask import Flask, request, jsonify, session
from flask_cors import CORS
from sqlalchemy.orm import Session
import os

from backend.database import engine, SessionLocal, Base
from backend.models import Student, Material, Bookmark, Progress
from backend.services.auth import authenticate_student, create_student
from backend.services.session import get_session, create_session, delete_session
from backend.services.notion_sync import notion_service

# Create database tables
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://localhost:5000"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_student_id():
    """Get current student ID from session."""
    session_data = get_session(request)
    return session_data.get("student_id") if session_data else None

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json
    db = SessionLocal()
    try:
        student = authenticate_student(db, data.get("email"), data.get("password"))
        if not student:
            return jsonify({"error": "Invalid email or password"}), 401
        
        token = create_session(student.id)
        response = jsonify({"success": True, "student": {"id": student.id, "email": student.email, "name": student.name}})
        response.set_cookie("session_token", token, httponly=True, max_age=604800)
        session["session_token"] = token
        return response
    finally:
        db.close()

@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.json
    db = SessionLocal()
    try:
        student = create_student(db, data.get("email"), data.get("name"), data.get("password"))
        token = create_session(student.id)
        response = jsonify({"success": True, "student": {"id": student.id, "email": student.email, "name": student.name}})
        response.set_cookie("session_token", token, httponly=True, max_age=604800)
        session["session_token"] = token
        return response
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    token = request.cookies.get("session_token") or session.get("session_token")
    if token:
        delete_session(token)
    response = jsonify({"success": True})
    response.delete_cookie("session_token")
    session.pop("session_token", None)
    return response

@app.route("/api/auth/me", methods=["GET"])
def get_current_user():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return jsonify({"error": "Student not found"}), 404
        return jsonify({"id": student.id, "email": student.email, "name": student.name})
    finally:
        db.close()

@app.route("/api/materials", methods=["GET"])
def get_materials():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        materials = db.query(Material).order_by(Material.order_index, Material.created_at).all()
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
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
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
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
