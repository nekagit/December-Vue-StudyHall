from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os

from backend.database import engine, SessionLocal, Base
from backend.models import Student, Material, MaterialProgress, Bookmark
from backend.services.auth import authenticate_student, create_student
from backend.services.session import get_session, create_session, delete_session
from backend.services.notion_sync import notion_service
from sqlalchemy import func, or_, and_
from datetime import datetime

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
        # Get query parameters
        search = request.args.get("search", "").strip()
        category = request.args.get("category", "").strip()
        
        query = db.query(Material)
        
        # Apply search filter
        if search:
            query = query.filter(
                or_(
                    Material.title.ilike(f"%{search}%"),
                    Material.content.ilike(f"%{search}%")
                )
            )
        
        # Apply category filter
        if category:
            query = query.filter(Material.category == category)
        
        materials = query.order_by(Material.order_index, Material.created_at).all()
        
        # Get progress and bookmark status for each material
        progress_map = {
            p.material_id: {
                "is_completed": p.is_completed,
                "progress_percentage": p.progress_percentage,
                "last_accessed_at": p.last_accessed_at.isoformat() if p.last_accessed_at else None
            }
            for p in db.query(MaterialProgress).filter(MaterialProgress.student_id == student_id).all()
        }
        
        bookmark_ids = {
            b.material_id for b in db.query(Bookmark).filter(Bookmark.student_id == student_id).all()
        }
        
        return jsonify([{
            "id": m.id,
            "title": m.title,
            "content": m.content,
            "category": m.category,
            "notion_url": m.notion_url,
            "created_at": m.created_at.isoformat() if m.created_at else None,
            "progress": progress_map.get(m.id, {"is_completed": False, "progress_percentage": 0, "last_accessed_at": None}),
            "is_bookmarked": m.id in bookmark_ids
        } for m in materials])
    finally:
        db.close()

@app.route("/api/materials/categories", methods=["GET"])
def get_categories():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        categories = db.query(Material.category).distinct().filter(Material.category.isnot(None)).all()
        return jsonify([cat[0] for cat in categories if cat[0]])
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
        
        # Update last accessed time
        progress = db.query(MaterialProgress).filter(
            and_(MaterialProgress.student_id == student_id, MaterialProgress.material_id == material_id)
        ).first()
        
        if progress:
            progress.last_accessed_at = datetime.utcnow()
        else:
            progress = MaterialProgress(
                student_id=student_id,
                material_id=material_id,
                last_accessed_at=datetime.utcnow()
            )
            db.add(progress)
        
        db.commit()
        
        # Get progress and bookmark status
        progress_data = {
            "is_completed": progress.is_completed,
            "progress_percentage": progress.progress_percentage,
            "last_accessed_at": progress.last_accessed_at.isoformat() if progress.last_accessed_at else None
        }
        
        is_bookmarked = db.query(Bookmark).filter(
            and_(Bookmark.student_id == student_id, Bookmark.material_id == material_id)
        ).first() is not None
        
        return jsonify({
            "id": material.id,
            "title": material.title,
            "content": material.content,
            "category": material.category,
            "notion_url": material.notion_url,
            "created_at": material.created_at.isoformat() if material.created_at else None,
            "progress": progress_data,
            "is_bookmarked": is_bookmarked
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

# Progress tracking endpoints
@app.route("/api/progress/<int:material_id>", methods=["POST", "PUT"])
def update_progress(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        data = request.json
        progress = db.query(MaterialProgress).filter(
            and_(MaterialProgress.student_id == student_id, MaterialProgress.material_id == material_id)
        ).first()
        
        if not progress:
            progress = MaterialProgress(
                student_id=student_id,
                material_id=material_id
            )
            db.add(progress)
        
        if "is_completed" in data:
            progress.is_completed = data["is_completed"]
            if data["is_completed"]:
                progress.completed_at = datetime.utcnow()
                progress.progress_percentage = 100
            else:
                progress.completed_at = None
        
        if "progress_percentage" in data:
            progress.progress_percentage = max(0, min(100, data["progress_percentage"]))
            if progress.progress_percentage == 100:
                progress.is_completed = True
                progress.completed_at = datetime.utcnow()
        
        db.commit()
        
        return jsonify({
            "success": True,
            "progress": {
                "is_completed": progress.is_completed,
                "progress_percentage": progress.progress_percentage,
                "last_accessed_at": progress.last_accessed_at.isoformat() if progress.last_accessed_at else None,
                "completed_at": progress.completed_at.isoformat() if progress.completed_at else None
            }
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Bookmark endpoints
@app.route("/api/bookmarks", methods=["GET"])
def get_bookmarks():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        bookmarks = db.query(Bookmark).filter(Bookmark.student_id == student_id).all()
        material_ids = [b.material_id for b in bookmarks]
        
        if not material_ids:
            return jsonify([])
        
        materials = db.query(Material).filter(Material.id.in_(material_ids)).all()
        return jsonify([{
            "id": m.id,
            "title": m.title,
            "content": m.content[:150] + "..." if m.content and len(m.content) > 150 else m.content,
            "category": m.category,
            "notion_url": m.notion_url,
            "created_at": m.created_at.isoformat() if m.created_at else None
        } for m in materials])
    finally:
        db.close()

@app.route("/api/bookmarks/<int:material_id>", methods=["POST"])
def add_bookmark(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        # Check if material exists
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            return jsonify({"error": "Material not found"}), 404
        
        # Check if bookmark already exists
        existing = db.query(Bookmark).filter(
            and_(Bookmark.student_id == student_id, Bookmark.material_id == material_id)
        ).first()
        
        if existing:
            return jsonify({"success": True, "message": "Already bookmarked"})
        
        bookmark = Bookmark(student_id=student_id, material_id=material_id)
        db.add(bookmark)
        db.commit()
        
        return jsonify({"success": True})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/bookmarks/<int:material_id>", methods=["DELETE"])
def remove_bookmark(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        bookmark = db.query(Bookmark).filter(
            and_(Bookmark.student_id == student_id, Bookmark.material_id == material_id)
        ).first()
        
        if bookmark:
            db.delete(bookmark)
            db.commit()
        
        return jsonify({"success": True})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Profile endpoints
@app.route("/api/profile", methods=["GET"])
def get_profile():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return jsonify({"error": "Student not found"}), 404
        
        # Get stats
        total_materials = db.query(Material).count()
        completed_materials = db.query(MaterialProgress).filter(
            and_(MaterialProgress.student_id == student_id, MaterialProgress.is_completed == True)
        ).count()
        bookmarks_count = db.query(Bookmark).filter(Bookmark.student_id == student_id).count()
        
        return jsonify({
            "id": student.id,
            "email": student.email,
            "name": student.name,
            "created_at": student.created_at.isoformat() if student.created_at else None,
            "stats": {
                "total_materials": total_materials,
                "completed_materials": completed_materials,
                "bookmarks_count": bookmarks_count,
                "completion_rate": round((completed_materials / total_materials * 100) if total_materials > 0 else 0, 1)
            }
        })
    finally:
        db.close()

@app.route("/api/profile", methods=["PUT"])
def update_profile():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return jsonify({"error": "Student not found"}), 404
        
        data = request.json
        
        if "name" in data:
            student.name = data["name"]
        
        if "email" in data:
            # Check if email is already taken
            existing = db.query(Student).filter(
                and_(Student.email == data["email"], Student.id != student_id)
            ).first()
            if existing:
                return jsonify({"error": "Email already taken"}), 400
            student.email = data["email"]
        
        if "password" in data and data["password"]:
            from backend.services.auth import hash_password
            student.password_hash = hash_password(data["password"])
        
        db.commit()
        
        return jsonify({
            "success": True,
            "student": {
                "id": student.id,
                "email": student.email,
                "name": student.name
            }
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Dashboard stats endpoint
@app.route("/api/dashboard/stats", methods=["GET"])
def get_dashboard_stats():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        total_materials = db.query(Material).count()
        completed_materials = db.query(MaterialProgress).filter(
            and_(MaterialProgress.student_id == student_id, MaterialProgress.is_completed == True)
        ).count()
        in_progress_materials = db.query(MaterialProgress).filter(
            and_(
                MaterialProgress.student_id == student_id,
                MaterialProgress.is_completed == False,
                MaterialProgress.progress_percentage > 0
            )
        ).count()
        bookmarks_count = db.query(Bookmark).filter(Bookmark.student_id == student_id).count()
        
        # Recent activity (last 5 accessed materials)
        recent_progress = db.query(MaterialProgress).filter(
            MaterialProgress.student_id == student_id
        ).order_by(MaterialProgress.last_accessed_at.desc()).limit(5).all()
        
        recent_materials = []
        for prog in recent_progress:
            material = db.query(Material).filter(Material.id == prog.material_id).first()
            if material:
                recent_materials.append({
                    "id": material.id,
                    "title": material.title,
                    "category": material.category,
                    "progress_percentage": prog.progress_percentage,
                    "is_completed": prog.is_completed,
                    "last_accessed_at": prog.last_accessed_at.isoformat() if prog.last_accessed_at else None
                })
        
        return jsonify({
            "total_materials": total_materials,
            "completed_materials": completed_materials,
            "in_progress_materials": in_progress_materials,
            "not_started_materials": total_materials - completed_materials - in_progress_materials,
            "bookmarks_count": bookmarks_count,
            "completion_rate": round((completed_materials / total_materials * 100) if total_materials > 0 else 0, 1),
            "recent_activity": recent_materials
        })
    finally:
        db.close()

# Test endpoints
@app.route("/api/tests/backend/run", methods=["POST"])
def run_backend_tests_endpoint():
    """Run backend tests."""
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    result = run_backend_tests()
    return jsonify(result)

@app.route("/api/tests/backend/coverage", methods=["GET"])
def get_backend_coverage_endpoint():
    """Get backend coverage data."""
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    coverage = get_backend_coverage()
    return jsonify(coverage)

@app.route("/api/tests/frontend/run", methods=["POST"])
def run_frontend_tests_endpoint():
    """Run frontend tests."""
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    result = run_frontend_tests()
    return jsonify(result)

@app.route("/api/tests/frontend/coverage", methods=["GET"])
def get_frontend_coverage_endpoint():
    """Get frontend coverage data."""
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    coverage = get_frontend_coverage()
    return jsonify(coverage)

@app.route("/api/tests/summary", methods=["GET"])
def get_tests_summary():
    """Get summary of all tests and coverage."""
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    backend_coverage = get_backend_coverage()
    frontend_coverage = get_frontend_coverage()
    
    return jsonify({
        "backend": {
            "coverage": backend_coverage
        },
        "frontend": {
            "coverage": frontend_coverage
        }
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
