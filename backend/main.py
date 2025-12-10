from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os

from backend.database import engine, SessionLocal, Base
from backend.models import Student, Material, Bookmark, Progress, StudySession, StudyGoal, Note, Rating, StudyStreak
from backend.services.auth import authenticate_student, create_student
from backend.services.session import get_session, create_session, delete_session
from backend.services.notion_sync import notion_service

# Create database tables
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# CORS configuration - more permissive for development
CORS(app, 
     supports_credentials=True, 
     origins=["http://localhost:5173", "http://localhost:5001", "http://127.0.0.1:5173"],
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
        response.set_cookie("session_token", token, httponly=True, max_age=604800, samesite="Lax", secure=False)
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
        
        # Get bookmark IDs for current student
        bookmark_ids = {b.material_id for b in db.query(Bookmark).filter(Bookmark.student_id == student_id).all()}
        
        return jsonify([{
            "id": m.id,
            "title": m.title,
            "content": m.content,
            "category": m.category,
            "notion_url": m.notion_url,
            "created_at": m.created_at.isoformat() if m.created_at else None,
            "is_bookmarked": m.id in bookmark_ids
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
        
        # Check if bookmarked
        bookmark = db.query(Bookmark).filter(
            Bookmark.student_id == student_id,
            Bookmark.material_id == material_id
        ).first()
        
        # Get progress
        progress = db.query(Progress).filter(
            Progress.student_id == student_id,
            Progress.material_id == material_id
        ).first()
        
        result = {
            "id": material.id,
            "title": material.title,
            "content": material.content,
            "category": material.category,
            "notion_url": material.notion_url,
            "created_at": material.created_at.isoformat() if material.created_at else None,
            "is_bookmarked": bookmark is not None,
            "bookmark_id": bookmark.id if bookmark else None,
            "progress": {
                "status": progress.status if progress else "not_started",
                "progress_percentage": progress.progress_percentage if progress else 0.0
            }
        }
        
        return jsonify(result)
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

# Bookmarks endpoints
@app.route("/api/bookmarks", methods=["GET"])
def get_bookmarks():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        bookmarks = db.query(Bookmark).filter(Bookmark.student_id == student_id).order_by(Bookmark.created_at.desc()).all()
        return jsonify([{
            "id": b.id,
            "material_id": b.material_id,
            "material": {
                "id": b.material.id,
                "title": b.material.title,
                "category": b.material.category,
                "created_at": b.material.created_at.isoformat() if b.material.created_at else None
            },
            "created_at": b.created_at.isoformat() if b.created_at else None
        } for b in bookmarks])
    finally:
        db.close()

@app.route("/api/bookmarks", methods=["POST"])
def create_bookmark():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    material_id = data.get("material_id")
    if not material_id:
        return jsonify({"error": "material_id is required"}), 400
    
    db = SessionLocal()
    try:
        # Check if material exists
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            return jsonify({"error": "Material not found"}), 404
        
        # Check if bookmark already exists
        existing = db.query(Bookmark).filter(
            Bookmark.student_id == student_id,
            Bookmark.material_id == material_id
        ).first()
        if existing:
            return jsonify({"error": "Bookmark already exists"}), 400
        
        bookmark = Bookmark(student_id=student_id, material_id=material_id)
        db.add(bookmark)
        db.commit()
        
        return jsonify({
            "success": True,
            "bookmark": {
                "id": bookmark.id,
                "material_id": bookmark.material_id,
                "created_at": bookmark.created_at.isoformat() if bookmark.created_at else None
            }
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/bookmarks/<int:bookmark_id>", methods=["DELETE"])
def delete_bookmark(bookmark_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        bookmark = db.query(Bookmark).filter(
            Bookmark.id == bookmark_id,
            Bookmark.student_id == student_id
        ).first()
        
        if not bookmark:
            return jsonify({"error": "Bookmark not found"}), 404
        
        db.delete(bookmark)
        db.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/bookmarks/material/<int:material_id>", methods=["DELETE"])
def delete_bookmark_by_material(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        bookmark = db.query(Bookmark).filter(
            Bookmark.material_id == material_id,
            Bookmark.student_id == student_id
        ).first()
        
        if not bookmark:
            return jsonify({"error": "Bookmark not found"}), 404
        
        db.delete(bookmark)
        db.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Progress endpoints
@app.route("/api/progress", methods=["GET"])
def get_progress():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        progress_records = db.query(Progress).filter(Progress.student_id == student_id).all()
        return jsonify([{
            "id": p.id,
            "material_id": p.material_id,
            "material": {
                "id": p.material.id,
                "title": p.material.title,
                "category": p.material.category
            },
            "status": p.status,
            "progress_percentage": p.progress_percentage,
            "last_accessed_at": p.last_accessed_at.isoformat() if p.last_accessed_at else None,
            "completed_at": p.completed_at.isoformat() if p.completed_at else None
        } for p in progress_records])
    finally:
        db.close()

@app.route("/api/progress/material/<int:material_id>", methods=["GET"])
def get_material_progress(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        progress = db.query(Progress).filter(
            Progress.student_id == student_id,
            Progress.material_id == material_id
        ).first()
        
        if not progress:
            return jsonify({
                "material_id": material_id,
                "status": "not_started",
                "progress_percentage": 0.0,
                "last_accessed_at": None,
                "completed_at": None
            })
        
        return jsonify({
            "id": progress.id,
            "material_id": progress.material_id,
            "status": progress.status,
            "progress_percentage": progress.progress_percentage,
            "last_accessed_at": progress.last_accessed_at.isoformat() if progress.last_accessed_at else None,
            "completed_at": progress.completed_at.isoformat() if progress.completed_at else None
        })
    finally:
        db.close()

@app.route("/api/progress/material/<int:material_id>", methods=["POST", "PUT"])
def update_progress(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    status = data.get("status", "in_progress")
    progress_percentage = data.get("progress_percentage", 0.0)
    
    # Validate status
    if status not in ["not_started", "in_progress", "completed"]:
        return jsonify({"error": "Invalid status"}), 400
    
    # Validate progress_percentage
    if not isinstance(progress_percentage, (int, float)) or progress_percentage < 0 or progress_percentage > 100:
        return jsonify({"error": "progress_percentage must be between 0 and 100"}), 400
    
    db = SessionLocal()
    try:
        # Check if material exists
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            return jsonify({"error": "Material not found"}), 404
        
        # Get or create progress record
        progress = db.query(Progress).filter(
            Progress.student_id == student_id,
            Progress.material_id == material_id
        ).first()
        
        from datetime import datetime
        if not progress:
            progress = Progress(
                student_id=student_id,
                material_id=material_id,
                status=status,
                progress_percentage=progress_percentage
            )
            db.add(progress)
        else:
            progress.status = status
            progress.progress_percentage = progress_percentage
            progress.last_accessed_at = datetime.utcnow()
            if status == "completed" and not progress.completed_at:
                progress.completed_at = datetime.utcnow()
        
        db.commit()
        
        return jsonify({
            "success": True,
            "progress": {
                "id": progress.id,
                "material_id": progress.material_id,
                "status": progress.status,
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

# Dashboard stats endpoint
@app.route("/api/dashboard/stats", methods=["GET"])
def get_dashboard_stats():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        from sqlalchemy import func
        
        # Total materials
        total_materials = db.query(func.count(Material.id)).scalar() or 0
        
        # Total bookmarks
        total_bookmarks = db.query(func.count(Bookmark.id)).filter(Bookmark.student_id == student_id).scalar() or 0
        
        # Progress stats
        completed_count = db.query(func.count(Progress.id)).filter(
            Progress.student_id == student_id,
            Progress.status == "completed"
        ).scalar() or 0
        
        in_progress_count = db.query(func.count(Progress.id)).filter(
            Progress.student_id == student_id,
            Progress.status == "in_progress"
        ).scalar() or 0
        
        # Recent bookmarks (last 5)
        recent_bookmarks = db.query(Bookmark).filter(
            Bookmark.student_id == student_id
        ).order_by(Bookmark.created_at.desc()).limit(5).all()
        
        # Recent progress updates (last 5)
        recent_progress = db.query(Progress).filter(
            Progress.student_id == student_id
        ).order_by(Progress.last_accessed_at.desc()).limit(5).all()
        
        return jsonify({
            "total_materials": total_materials,
            "total_bookmarks": total_bookmarks,
            "completed_materials": completed_count,
            "in_progress_materials": in_progress_count,
            "recent_bookmarks": [{
                "id": b.id,
                "material": {
                    "id": b.material.id,
                    "title": b.material.title,
                    "category": b.material.category
                },
                "created_at": b.created_at.isoformat() if b.created_at else None
            } for b in recent_bookmarks],
            "recent_progress": [{
                "id": p.id,
                "material": {
                    "id": p.material.id,
                    "title": p.material.title,
                    "category": p.material.category
                },
                "status": p.status,
                "progress_percentage": p.progress_percentage,
                "last_accessed_at": p.last_accessed_at.isoformat() if p.last_accessed_at else None
            } for p in recent_progress]
        })
    finally:
        db.close()

# Categories endpoint
@app.route("/api/materials/categories", methods=["GET"])
def get_categories():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        from sqlalchemy import distinct
        categories = db.query(distinct(Material.category)).filter(Material.category.isnot(None)).all()
        return jsonify([cat[0] for cat in categories if cat[0]])
    finally:
        db.close()

# Study Goals endpoints
@app.route("/api/goals", methods=["GET"])
def get_goals():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        goals = db.query(StudyGoal).filter(StudyGoal.student_id == student_id).order_by(StudyGoal.created_at.desc()).all()
        return jsonify([{
            "id": g.id,
            "title": g.title,
            "description": g.description,
            "target_date": g.target_date.isoformat() if g.target_date else None,
            "is_completed": g.is_completed,
            "completed_at": g.completed_at.isoformat() if g.completed_at else None,
            "created_at": g.created_at.isoformat() if g.created_at else None
        } for g in goals])
    finally:
        db.close()

@app.route("/api/goals", methods=["POST"])
def create_goal():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400
    
    db = SessionLocal()
    try:
        from datetime import datetime
        target_date = None
        if data.get("target_date"):
            target_date = datetime.fromisoformat(data["target_date"].replace("Z", "+00:00"))
        
        goal = StudyGoal(
            student_id=student_id,
            title=title,
            description=data.get("description"),
            target_date=target_date
        )
        db.add(goal)
        db.commit()
        
        return jsonify({
            "success": True,
            "goal": {
                "id": goal.id,
                "title": goal.title,
                "description": goal.description,
                "target_date": goal.target_date.isoformat() if goal.target_date else None,
                "is_completed": goal.is_completed,
                "created_at": goal.created_at.isoformat() if goal.created_at else None
            }
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/goals/<int:goal_id>", methods=["PUT"])
def update_goal(goal_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    db = SessionLocal()
    try:
        goal = db.query(StudyGoal).filter(
            StudyGoal.id == goal_id,
            StudyGoal.student_id == student_id
        ).first()
        
        if not goal:
            return jsonify({"error": "Goal not found"}), 404
        
        if "title" in data:
            goal.title = data["title"]
        if "description" in data:
            goal.description = data["description"]
        if "target_date" in data:
            from datetime import datetime
            goal.target_date = datetime.fromisoformat(data["target_date"].replace("Z", "+00:00")) if data["target_date"] else None
        if "is_completed" in data:
            goal.is_completed = data["is_completed"]
            if data["is_completed"] and not goal.completed_at:
                from datetime import datetime
                goal.completed_at = datetime.utcnow()
            elif not data["is_completed"]:
                goal.completed_at = None
        
        db.commit()
        
        return jsonify({
            "success": True,
            "goal": {
                "id": goal.id,
                "title": goal.title,
                "description": goal.description,
                "target_date": goal.target_date.isoformat() if goal.target_date else None,
                "is_completed": goal.is_completed,
                "completed_at": goal.completed_at.isoformat() if goal.completed_at else None,
                "created_at": goal.created_at.isoformat() if goal.created_at else None
            }
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/goals/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        goal = db.query(StudyGoal).filter(
            StudyGoal.id == goal_id,
            StudyGoal.student_id == student_id
        ).first()
        
        if not goal:
            return jsonify({"error": "Goal not found"}), 404
        
        db.delete(goal)
        db.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Study Sessions endpoints
@app.route("/api/sessions", methods=["GET"])
def get_sessions():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        sessions = db.query(StudySession).filter(StudySession.student_id == student_id).order_by(StudySession.created_at.desc()).limit(50).all()
        return jsonify([{
            "id": s.id,
            "material_id": s.material_id,
            "material": {
                "id": s.material.id,
                "title": s.material.title,
                "category": s.material.category
            } if s.material else None,
            "duration_minutes": s.duration_minutes,
            "notes": s.notes,
            "started_at": s.started_at.isoformat() if s.started_at else None,
            "ended_at": s.ended_at.isoformat() if s.ended_at else None,
            "created_at": s.created_at.isoformat() if s.created_at else None
        } for s in sessions])
    finally:
        db.close()

@app.route("/api/sessions", methods=["POST"])
def create_session():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    duration_minutes = data.get("duration_minutes")
    if not duration_minutes or duration_minutes <= 0:
        return jsonify({"error": "duration_minutes is required and must be positive"}), 400
    
    db = SessionLocal()
    try:
        from datetime import datetime
        
        # Update study streak
        streak = db.query(StudyStreak).filter(StudyStreak.student_id == student_id).first()
        today = datetime.utcnow().date()
        
        if not streak:
            streak = StudyStreak(
                student_id=student_id,
                current_streak=1,
                longest_streak=1,
                last_study_date=datetime.utcnow()
            )
            db.add(streak)
        else:
            last_date = streak.last_study_date.date() if streak.last_study_date else None
            if last_date != today:
                # Check if yesterday
                from datetime import timedelta
                yesterday = today - timedelta(days=1)
                if last_date == yesterday:
                    streak.current_streak += 1
                else:
                    streak.current_streak = 1
                
                if streak.current_streak > streak.longest_streak:
                    streak.longest_streak = streak.current_streak
                
                streak.last_study_date = datetime.utcnow()
        
        session = StudySession(
            student_id=student_id,
            material_id=data.get("material_id"),
            duration_minutes=duration_minutes,
            notes=data.get("notes"),
            started_at=datetime.fromisoformat(data["started_at"].replace("Z", "+00:00")) if data.get("started_at") else datetime.utcnow(),
            ended_at=datetime.fromisoformat(data["ended_at"].replace("Z", "+00:00")) if data.get("ended_at") else datetime.utcnow()
        )
        db.add(session)
        db.commit()
        
        return jsonify({
            "success": True,
            "session": {
                "id": session.id,
                "material_id": session.material_id,
                "duration_minutes": session.duration_minutes,
                "notes": session.notes,
                "started_at": session.started_at.isoformat() if session.started_at else None,
                "ended_at": session.ended_at.isoformat() if session.ended_at else None
            }
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Notes endpoints
@app.route("/api/notes", methods=["GET"])
def get_notes():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        material_id = request.args.get("material_id", type=int)
        query = db.query(Note).filter(Note.student_id == student_id)
        if material_id:
            query = query.filter(Note.material_id == material_id)
        
        notes = query.order_by(Note.created_at.desc()).all()
        return jsonify([{
            "id": n.id,
            "material_id": n.material_id,
            "material": {
                "id": n.material.id,
                "title": n.material.title,
                "category": n.material.category
            },
            "title": n.title,
            "content": n.content,
            "created_at": n.created_at.isoformat() if n.created_at else None,
            "updated_at": n.updated_at.isoformat() if n.updated_at else None
        } for n in notes])
    finally:
        db.close()

@app.route("/api/notes", methods=["POST"])
def create_note():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    material_id = data.get("material_id")
    content = data.get("content")
    
    if not material_id:
        return jsonify({"error": "material_id is required"}), 400
    if not content:
        return jsonify({"error": "content is required"}), 400
    
    db = SessionLocal()
    try:
        # Check if material exists
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            return jsonify({"error": "Material not found"}), 404
        
        note = Note(
            student_id=student_id,
            material_id=material_id,
            title=data.get("title"),
            content=content
        )
        db.add(note)
        db.commit()
        
        return jsonify({
            "success": True,
            "note": {
                "id": note.id,
                "material_id": note.material_id,
                "title": note.title,
                "content": note.content,
                "created_at": note.created_at.isoformat() if note.created_at else None
            }
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    db = SessionLocal()
    try:
        note = db.query(Note).filter(
            Note.id == note_id,
            Note.student_id == student_id
        ).first()
        
        if not note:
            return jsonify({"error": "Note not found"}), 404
        
        if "title" in data:
            note.title = data["title"]
        if "content" in data:
            note.content = data["content"]
        
        db.commit()
        
        return jsonify({
            "success": True,
            "note": {
                "id": note.id,
                "material_id": note.material_id,
                "title": note.title,
                "content": note.content,
                "created_at": note.created_at.isoformat() if note.created_at else None,
                "updated_at": note.updated_at.isoformat() if note.updated_at else None
            }
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        note = db.query(Note).filter(
            Note.id == note_id,
            Note.student_id == student_id
        ).first()
        
        if not note:
            return jsonify({"error": "Note not found"}), 404
        
        db.delete(note)
        db.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Ratings endpoints
@app.route("/api/ratings", methods=["GET"])
def get_ratings():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        material_id = request.args.get("material_id", type=int)
        query = db.query(Rating).filter(Rating.student_id == student_id)
        if material_id:
            query = query.filter(Rating.material_id == material_id)
        
        ratings = query.order_by(Rating.created_at.desc()).all()
        return jsonify([{
            "id": r.id,
            "material_id": r.material_id,
            "material": {
                "id": r.material.id,
                "title": r.material.title,
                "category": r.material.category
            },
            "rating": r.rating,
            "comment": r.comment,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None
        } for r in ratings])
    finally:
        db.close()

@app.route("/api/ratings", methods=["POST"])
def create_rating():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    material_id = data.get("material_id")
    rating = data.get("rating")
    
    if not material_id:
        return jsonify({"error": "material_id is required"}), 400
    if not rating or rating < 1 or rating > 5:
        return jsonify({"error": "rating is required and must be between 1 and 5"}), 400
    
    db = SessionLocal()
    try:
        # Check if material exists
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            return jsonify({"error": "Material not found"}), 404
        
        # Check if rating already exists
        existing = db.query(Rating).filter(
            Rating.student_id == student_id,
            Rating.material_id == material_id
        ).first()
        
        if existing:
            existing.rating = rating
            existing.comment = data.get("comment")
            db.commit()
            return jsonify({
                "success": True,
                "rating": {
                    "id": existing.id,
                    "material_id": existing.material_id,
                    "rating": existing.rating,
                    "comment": existing.comment,
                    "created_at": existing.created_at.isoformat() if existing.created_at else None,
                    "updated_at": existing.updated_at.isoformat() if existing.updated_at else None
                }
            })
        
        rating_obj = Rating(
            student_id=student_id,
            material_id=material_id,
            rating=rating,
            comment=data.get("comment")
        )
        db.add(rating_obj)
        db.commit()
        
        return jsonify({
            "success": True,
            "rating": {
                "id": rating_obj.id,
                "material_id": rating_obj.material_id,
                "rating": rating_obj.rating,
                "comment": rating_obj.comment,
                "created_at": rating_obj.created_at.isoformat() if rating_obj.created_at else None
            }
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/ratings/<int:rating_id>", methods=["DELETE"])
def delete_rating(rating_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        rating = db.query(Rating).filter(
            Rating.id == rating_id,
            Rating.student_id == student_id
        ).first()
        
        if not rating:
            return jsonify({"error": "Rating not found"}), 404
        
        db.delete(rating)
        db.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Study Streak endpoint
@app.route("/api/streak", methods=["GET"])
def get_streak():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        streak = db.query(StudyStreak).filter(StudyStreak.student_id == student_id).first()
        
        if not streak:
            return jsonify({
                "current_streak": 0,
                "longest_streak": 0,
                "last_study_date": None
            })
        
        return jsonify({
            "current_streak": streak.current_streak,
            "longest_streak": streak.longest_streak,
            "last_study_date": streak.last_study_date.isoformat() if streak.last_study_date else None
        })
    finally:
        db.close()

# Study Sessions endpoints
@app.route("/api/study-sessions", methods=["GET"])
def get_study_sessions():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        sessions = db.query(StudySession).filter(StudySession.student_id == student_id).order_by(StudySession.created_at.desc()).all()
        return jsonify([{
            "id": s.id,
            "material_id": s.material_id,
            "material": {
                "id": s.material.id,
                "title": s.material.title,
                "category": s.material.category
            } if s.material else None,
            "duration_minutes": s.duration_minutes,
            "notes": s.notes,
            "started_at": s.started_at.isoformat() if s.started_at else None,
            "ended_at": s.ended_at.isoformat() if s.ended_at else None,
            "created_at": s.created_at.isoformat() if s.created_at else None
        } for s in sessions])
    finally:
        db.close()

@app.route("/api/study-sessions", methods=["POST"])
def create_study_session():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    material_id = data.get("material_id")  # Optional
    notes = data.get("notes")
    
    db = SessionLocal()
    try:
        from datetime import datetime
        session = StudySession(
            student_id=student_id,
            material_id=material_id,
            notes=notes,
            started_at=datetime.utcnow(),
            duration_minutes=0.0
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return jsonify({
            "success": True,
            "session": {
                "id": session.id,
                "material_id": session.material_id,
                "duration_minutes": session.duration_minutes,
                "notes": session.notes,
                "started_at": session.started_at.isoformat() if session.started_at else None,
                "ended_at": session.ended_at.isoformat() if session.ended_at else None
            }
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/study-sessions/<int:session_id>", methods=["PUT"])
def update_study_session(session_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    duration_minutes = data.get("duration_minutes")
    notes = data.get("notes")
    ended = data.get("ended", False)
    
    db = SessionLocal()
    try:
        session = db.query(StudySession).filter(
            StudySession.id == session_id,
            StudySession.student_id == student_id
        ).first()
        
        if not session:
            return jsonify({"error": "Session not found"}), 404
        
        if duration_minutes is not None:
            session.duration_minutes = duration_minutes
        if notes is not None:
            session.notes = notes
        if ended:
            from datetime import datetime
            session.ended_at = datetime.utcnow()
        
        db.commit()
        
        return jsonify({
            "success": True,
            "session": {
                "id": session.id,
                "material_id": session.material_id,
                "duration_minutes": session.duration_minutes,
                "notes": session.notes,
                "started_at": session.started_at.isoformat() if session.started_at else None,
                "ended_at": session.ended_at.isoformat() if session.ended_at else None
            }
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/study-sessions/<int:session_id>", methods=["DELETE"])
def delete_study_session(session_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        session = db.query(StudySession).filter(
            StudySession.id == session_id,
            StudySession.student_id == student_id
        ).first()
        
        if not session:
            return jsonify({"error": "Session not found"}), 404
        
        db.delete(session)
        db.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Notes endpoints
@app.route("/api/materials/<int:material_id>/notes", methods=["GET"])
def get_material_notes(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        notes = db.query(Note).filter(
            Note.student_id == student_id,
            Note.material_id == material_id
        ).order_by(Note.created_at.desc()).all()
        
        return jsonify([{
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "created_at": n.created_at.isoformat() if n.created_at else None,
            "updated_at": n.updated_at.isoformat() if n.updated_at else None
        } for n in notes])
    finally:
        db.close()

@app.route("/api/materials/<int:material_id>/notes", methods=["POST"])
def create_material_note(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    content = data.get("content")
    title = data.get("title")
    
    if not content:
        return jsonify({"error": "content is required"}), 400
    
    db = SessionLocal()
    try:
        # Check if material exists
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            return jsonify({"error": "Material not found"}), 404
        
        note = Note(
            student_id=student_id,
            material_id=material_id,
            title=title,
            content=content
        )
        db.add(note)
        db.commit()
        db.refresh(note)
        
        return jsonify({
            "success": True,
            "note": {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "created_at": note.created_at.isoformat() if note.created_at else None
            }
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Ratings endpoints
@app.route("/api/materials/<int:material_id>/rating", methods=["GET"])
def get_material_rating(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        # Get user's rating
        rating = db.query(Rating).filter(
            Rating.student_id == student_id,
            Rating.material_id == material_id
        ).first()
        
        # Get average rating
        from sqlalchemy import func
        avg_result = db.query(func.avg(Rating.rating)).filter(Rating.material_id == material_id).scalar()
        avg_rating = float(avg_result) if avg_result else None
        
        # Get total ratings count
        total_ratings = db.query(func.count(Rating.id)).filter(Rating.material_id == material_id).scalar() or 0
        
        return jsonify({
            "user_rating": {
                "id": rating.id,
                "rating": rating.rating,
                "comment": rating.comment
            } if rating else None,
            "average_rating": round(avg_rating, 2) if avg_rating else None,
            "total_ratings": total_ratings
        })
    finally:
        db.close()

@app.route("/api/materials/<int:material_id>/rating", methods=["POST", "PUT"])
def set_material_rating(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    rating_value = data.get("rating")
    comment = data.get("comment")
    
    if not rating_value or not isinstance(rating_value, int) or rating_value < 1 or rating_value > 5:
        return jsonify({"error": "rating must be between 1 and 5"}), 400
    
    db = SessionLocal()
    try:
        # Check if material exists
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            return jsonify({"error": "Material not found"}), 404
        
        # Get or create rating
        rating = db.query(Rating).filter(
            Rating.student_id == student_id,
            Rating.material_id == material_id
        ).first()
        
        if rating:
            rating.rating = rating_value
            if comment is not None:
                rating.comment = comment
        else:
            rating = Rating(
                student_id=student_id,
                material_id=material_id,
                rating=rating_value,
                comment=comment
            )
            db.add(rating)
        
        db.commit()
        
        # Get updated average
        from sqlalchemy import func
        avg_result = db.query(func.avg(Rating.rating)).filter(Rating.material_id == material_id).scalar()
        avg_rating = float(avg_result) if avg_result else None
        
        return jsonify({
            "success": True,
            "rating": {
                "id": rating.id,
                "rating": rating.rating,
                "comment": rating.comment
            },
            "average_rating": round(avg_rating, 2) if avg_rating else None
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Study Statistics endpoint
@app.route("/api/statistics", methods=["GET"])
def get_statistics():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        # Total study time (in minutes)
        total_study_time = db.query(func.sum(StudySession.duration_minutes)).filter(
            StudySession.student_id == student_id
        ).scalar() or 0.0
        
        # Study sessions count
        total_sessions = db.query(func.count(StudySession.id)).filter(
            StudySession.student_id == student_id
        ).scalar() or 0
        
        # Average session duration
        avg_duration = total_study_time / total_sessions if total_sessions > 0 else 0.0
        
        # Study time this week
        week_ago = datetime.utcnow() - timedelta(days=7)
        weekly_study_time = db.query(func.sum(StudySession.duration_minutes)).filter(
            StudySession.student_id == student_id,
            StudySession.created_at >= week_ago
        ).scalar() or 0.0
        
        # Study time today
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        daily_study_time = db.query(func.sum(StudySession.duration_minutes)).filter(
            StudySession.student_id == student_id,
            StudySession.created_at >= today_start
        ).scalar() or 0.0
        
        # Active goals count
        active_goals = db.query(func.count(StudyGoal.id)).filter(
            StudyGoal.student_id == student_id,
            StudyGoal.is_completed == False
        ).scalar() or 0
        
        # Completed goals count
        completed_goals = db.query(func.count(StudyGoal.id)).filter(
            StudyGoal.student_id == student_id,
            StudyGoal.is_completed == True
        ).scalar() or 0
        
        # Recent sessions (last 7)
        recent_sessions = db.query(StudySession).filter(
            StudySession.student_id == student_id
        ).order_by(StudySession.created_at.desc()).limit(7).all()
        
        return jsonify({
            "total_study_time_minutes": round(total_study_time, 2),
            "total_sessions": total_sessions,
            "average_session_duration": round(avg_duration, 2),
            "weekly_study_time_minutes": round(weekly_study_time, 2),
            "daily_study_time_minutes": round(daily_study_time, 2),
            "active_goals": active_goals,
            "completed_goals": completed_goals,
            "recent_sessions": [{
                "id": s.id,
                "material_id": s.material_id,
                "material_title": s.material.title if s.material else "General Study",
                "duration_minutes": s.duration_minutes,
                "created_at": s.created_at.isoformat() if s.created_at else None
            } for s in recent_sessions]
        })
    finally:
        db.close()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
