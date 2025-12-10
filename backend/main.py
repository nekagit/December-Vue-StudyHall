from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os

from backend.database import engine, SessionLocal, Base
from backend.models import Student, Material, Bookmark, Progress, Note, StudySession, LearningStreak
from backend.services.auth import authenticate_student, create_student
from backend.services.session import get_session, create_session, delete_session
from backend.services.notion_sync import notion_service

# Create database tables
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
CORS(app, 
     supports_credentials=True, 
     origins=["http://localhost:5173", "http://localhost:5000"],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

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
        
        # Get progress records for filtering
        progress_records = {p.material_id: p for p in db.query(Progress).filter(Progress.student_id == student_id).all()}
        
        # Progress status filter
        progress_status = request.args.get("progress_status", "").strip()
        if progress_status:
            if progress_status == "not_started":
                materials = [m for m in materials if m.id not in progress_records]
            elif progress_status == "in_progress":
                materials = [m for m in materials if m.id in progress_records and progress_records[m.id].status == "in_progress"]
            elif progress_status == "completed":
                materials = [m for m in materials if m.id in progress_records and progress_records[m.id].status == "completed"]
        
        # Calculate reading time (average reading speed: 200 words per minute)
        def calculate_reading_time(content):
            if not content:
                return 0
            word_count = len(content.split())
            return max(1, round(word_count / 200))  # At least 1 minute
        
        return jsonify([{
            "id": m.id,
            "title": m.title,
            "content": m.content,
            "category": m.category,
            "notion_url": m.notion_url,
            "created_at": m.created_at.isoformat() if m.created_at else None,
            "is_bookmarked": m.id in bookmark_ids,
            "reading_time_minutes": calculate_reading_time(m.content),
            "progress_status": progress_records[m.id].status if m.id in progress_records else "not_started"
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

# Notes endpoints
@app.route("/api/notes/material/<int:material_id>", methods=["GET"])
def get_material_notes(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        note = db.query(Note).filter(
            Note.student_id == student_id,
            Note.material_id == material_id
        ).first()
        
        if not note:
            return jsonify({"id": None, "content": "", "material_id": material_id})
        
        return jsonify({
            "id": note.id,
            "content": note.content,
            "material_id": note.material_id,
            "created_at": note.created_at.isoformat() if note.created_at else None,
            "updated_at": note.updated_at.isoformat() if note.updated_at else None
        })
    finally:
        db.close()

@app.route("/api/notes/material/<int:material_id>", methods=["POST", "PUT"])
def upsert_note(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"error": "Content is required"}), 400
    
    db = SessionLocal()
    try:
        # Check if material exists
        material = db.query(Material).filter(Material.id == material_id).first()
        if not material:
            return jsonify({"error": "Material not found"}), 404
        
        # Get or create note
        note = db.query(Note).filter(
            Note.student_id == student_id,
            Note.material_id == material_id
        ).first()
        
        from datetime import datetime
        if not note:
            note = Note(
                student_id=student_id,
                material_id=material_id,
                content=content
            )
            db.add(note)
        else:
            note.content = content
            note.updated_at = datetime.utcnow()
        
        db.commit()
        
        return jsonify({
            "success": True,
            "note": {
                "id": note.id,
                "content": note.content,
                "material_id": note.material_id,
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

# Study Session endpoints
@app.route("/api/study-sessions", methods=["POST"])
def create_study_session():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    duration_minutes = data.get("duration_minutes", 0.0)
    material_id = data.get("material_id")  # Optional
    
    if duration_minutes <= 0:
        return jsonify({"error": "Duration must be greater than 0"}), 400
    
    db = SessionLocal()
    try:
        # Validate material if provided
        if material_id:
            material = db.query(Material).filter(Material.id == material_id).first()
            if not material:
                return jsonify({"error": "Material not found"}), 404
        
        from datetime import datetime
        study_session = StudySession(
            student_id=student_id,
            material_id=material_id,
            duration_minutes=duration_minutes,
            started_at=datetime.utcnow()
        )
        db.add(study_session)
        db.commit()
        
        # Update learning streak
        update_learning_streak(db, student_id)
        
        return jsonify({
            "success": True,
            "session": {
                "id": study_session.id,
                "duration_minutes": study_session.duration_minutes,
                "material_id": study_session.material_id,
                "started_at": study_session.started_at.isoformat() if study_session.started_at else None
            }
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/study-sessions", methods=["GET"])
def get_study_sessions():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        from datetime import datetime
        from datetime import timedelta
        
        # Get date range filter
        days = request.args.get("days", type=int, default=30)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        sessions = db.query(StudySession).filter(
            StudySession.student_id == student_id,
            StudySession.started_at >= start_date
        ).order_by(StudySession.started_at.desc()).all()
        
        total_minutes = sum(s.duration_minutes for s in sessions)
        
        return jsonify({
            "sessions": [{
                "id": s.id,
                "duration_minutes": s.duration_minutes,
                "material_id": s.material_id,
                "material": {
                    "id": s.material.id,
                    "title": s.material.title
                } if s.material else None,
                "session_date": s.session_date.isoformat() if s.session_date else None
            } for s in sessions],
            "total_minutes": total_minutes,
            "total_hours": round(total_minutes / 60, 2)
        })
    finally:
        db.close()

def update_learning_streak(db, student_id):
    """Update learning streak for a student."""
    from datetime import datetime, date
    
    streak = db.query(LearningStreak).filter(LearningStreak.student_id == student_id).first()
    today = datetime.utcnow().date()
    
    if not streak:
        streak = LearningStreak(
            student_id=student_id,
            current_streak_days=1,
            longest_streak_days=1,
            last_study_date=datetime.utcnow()
        )
        db.add(streak)
    else:
        if streak.last_study_date:
            # Convert to date if it's a datetime
            if isinstance(streak.last_study_date, datetime):
                last_date = streak.last_study_date.date()
            elif isinstance(streak.last_study_date, date):
                last_date = streak.last_study_date
            else:
                last_date = today
            
            days_diff = (today - last_date).days
            
            if days_diff == 0:
                # Already studied today, no change
                pass
            elif days_diff == 1:
                # Consecutive day
                streak.current_streak_days += 1
                streak.longest_streak_days = max(streak.longest_streak_days, streak.current_streak_days)
            else:
                # Streak broken, start over
                streak.current_streak_days = 1
        else:
            # First time studying
            streak.current_streak_days = 1
            streak.longest_streak_days = max(streak.longest_streak_days, 1)
        
        streak.last_study_date = datetime.utcnow()
    
    db.commit()

# Learning Streak endpoints
@app.route("/api/learning-streak", methods=["GET"])
def get_learning_streak():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        streak = db.query(LearningStreak).filter(LearningStreak.student_id == student_id).first()
        
        if not streak:
            return jsonify({
                "current_streak_days": 0,
                "longest_streak_days": 0,
                "last_study_date": None
            })
        
        return jsonify({
            "current_streak_days": streak.current_streak_days,
            "longest_streak_days": streak.longest_streak_days,
            "last_study_date": streak.last_study_date.isoformat() if streak.last_study_date else None
        })
    finally:
        db.close()

# Ratings endpoints
@app.route("/api/ratings/material/<int:material_id>", methods=["GET"])
def get_material_rating(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        rating = db.query(Rating).filter(
            Rating.student_id == student_id,
            Rating.material_id == material_id
        ).first()
        
        # Get average rating for the material
        from sqlalchemy import func
        avg_result = db.query(func.avg(Rating.rating)).filter(
            Rating.material_id == material_id
        ).scalar()
        avg_rating = round(float(avg_result), 2) if avg_result else None
        
        # Get rating count
        rating_count = db.query(func.count(Rating.id)).filter(
            Rating.material_id == material_id
        ).scalar() or 0
        
        return jsonify({
            "user_rating": rating.rating if rating else None,
            "average_rating": avg_rating,
            "rating_count": rating_count
        })
    finally:
        db.close()

@app.route("/api/ratings/material/<int:material_id>", methods=["POST", "PUT"])
def set_rating(material_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    rating_value = data.get("rating")
    
    if not rating_value or not isinstance(rating_value, (int, float)):
        return jsonify({"error": "rating is required and must be a number"}), 400
    
    if rating_value < 1.0 or rating_value > 5.0:
        return jsonify({"error": "rating must be between 1.0 and 5.0"}), 400
    
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
            rating.rating = float(rating_value)
        else:
            rating = Rating(
                student_id=student_id,
                material_id=material_id,
                rating=float(rating_value)
            )
            db.add(rating)
        
        db.commit()
        
        # Get updated average
        from sqlalchemy import func
        avg_result = db.query(func.avg(Rating.rating)).filter(
            Rating.material_id == material_id
        ).scalar()
        avg_rating = round(float(avg_result), 2) if avg_result else None
        
        return jsonify({
            "success": True,
            "rating": {
                "id": rating.id,
                "rating": rating.rating,
                "average_rating": avg_rating
            }
        })
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
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
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    target_date_str = data.get("target_date")
    
    if not title:
        return jsonify({"error": "title is required"}), 400
    
    db = SessionLocal()
    try:
        from datetime import datetime
        target_date = None
        if target_date_str:
            try:
                target_date = datetime.fromisoformat(target_date_str.replace('Z', '+00:00'))
            except:
                return jsonify({"error": "Invalid target_date format"}), 400
        
        goal = StudyGoal(
            student_id=student_id,
            title=title,
            description=description,
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
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    target_date_str = data.get("target_date")
    is_completed = data.get("is_completed")
    
    db = SessionLocal()
    try:
        goal = db.query(StudyGoal).filter(
            StudyGoal.id == goal_id,
            StudyGoal.student_id == student_id
        ).first()
        
        if not goal:
            return jsonify({"error": "Goal not found"}), 404
        
        if title:
            goal.title = title
        if description is not None:
            goal.description = description
        if target_date_str is not None:
            if target_date_str:
                from datetime import datetime
                try:
                    goal.target_date = datetime.fromisoformat(target_date_str.replace('Z', '+00:00'))
                except:
                    return jsonify({"error": "Invalid target_date format"}), 400
            else:
                goal.target_date = None
        
        if is_completed is not None:
            goal.is_completed = is_completed
            if is_completed and not goal.completed_at:
                from datetime import datetime
                goal.completed_at = datetime.utcnow()
            elif not is_completed:
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
                "completed_at": goal.completed_at.isoformat() if goal.completed_at else None
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

# Study Stats endpoint
@app.route("/api/study-sessions/stats", methods=["GET"])
def get_study_stats():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        # Total study time
        total_time = db.query(func.sum(StudySession.duration_minutes)).filter(
            StudySession.student_id == student_id
        ).scalar() or 0.0
        
        # Today's study time
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_time = db.query(func.sum(StudySession.duration_minutes)).filter(
            StudySession.student_id == student_id,
            StudySession.session_date >= today_start
        ).scalar() or 0.0
        
        # This week's study time
        week_start = today_start - timedelta(days=7)
        week_time = db.query(func.sum(StudySession.duration_minutes)).filter(
            StudySession.student_id == student_id,
            StudySession.session_date >= week_start
        ).scalar() or 0.0
        
        # Get streak
        streak = db.query(LearningStreak).filter(LearningStreak.student_id == student_id).first()
        
        return jsonify({
            "total_study_time_minutes": round(float(total_time), 2),
            "today_study_time_minutes": round(float(today_time), 2),
            "week_study_time_minutes": round(float(week_time), 2),
            "current_streak_days": streak.current_streak_days if streak else 0,
            "longest_streak_days": streak.longest_streak_days if streak else 0
        })
    finally:
        db.close()

# Password change endpoint
@app.route("/api/auth/change-password", methods=["POST"])
def change_password():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    
    if not current_password or not new_password:
        return jsonify({"error": "current_password and new_password are required"}), 400
    
    if len(new_password) < 6:
        return jsonify({"error": "New password must be at least 6 characters"}), 400
    
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return jsonify({"error": "Student not found"}), 404
        
        # Verify current password
        if not verify_password(current_password, student.password_hash):
            return jsonify({"error": "Current password is incorrect"}), 400
        
        # Update password
        student.password_hash = hash_password(new_password)
        db.commit()
        
        return jsonify({"success": True, "message": "Password updated successfully"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Export progress endpoint
@app.route("/api/export/progress", methods=["GET"])
def export_progress():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        from datetime import datetime
        
        # Get all progress records
        progress_records = db.query(Progress).filter(Progress.student_id == student_id).all()
        
        # Get all bookmarks
        bookmarks = db.query(Bookmark).filter(Bookmark.student_id == student_id).all()
        
        # Get study sessions summary
        sessions = db.query(StudySession).filter(StudySession.student_id == student_id).all()
        total_study_minutes = sum(s.duration_minutes for s in sessions)
        
        # Get streak
        streak = db.query(LearningStreak).filter(LearningStreak.student_id == student_id).first()
        
        export_data = {
            "exported_at": datetime.utcnow().isoformat(),
            "student_id": student_id,
            "progress": [{
                "material_id": p.material_id,
                "material_title": p.material.title,
                "status": p.status,
                "progress_percentage": p.progress_percentage,
                "last_accessed_at": p.last_accessed_at.isoformat() if p.last_accessed_at else None,
                "completed_at": p.completed_at.isoformat() if p.completed_at else None
            } for p in progress_records],
            "bookmarks": [{
                "material_id": b.material_id,
                "material_title": b.material.title,
                "created_at": b.created_at.isoformat() if b.created_at else None
            } for b in bookmarks],
            "study_statistics": {
                "total_sessions": len(sessions),
                "total_study_minutes": total_study_minutes,
                "total_study_hours": round(total_study_minutes / 60, 2),
                "current_streak_days": streak.current_streak_days if streak else 0,
                "longest_streak_days": streak.longest_streak_days if streak else 0
            }
        }
        
        return jsonify(export_data)
    finally:
        db.close()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
