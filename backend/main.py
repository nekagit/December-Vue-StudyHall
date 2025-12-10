from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
import traceback

from backend.database import engine, SessionLocal, Base
from backend.models import Student, Material, Bookmark, Progress, StudySession, StudyStreak, Note, Rating, StudyGoal
from backend.services.notion_sync import notion_service

# Create database tables
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

# CORS configuration - more permissive for development
CORS(app, 
     supports_credentials=True, 
     origins=["http://localhost:5173", "http://localhost:5000", "http://127.0.0.1:5173"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With", "X-Character-Id", "X-Character-Name", "X-Character-Role"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     expose_headers=["Content-Type"])

# Add explicit OPTIONS handler for all routes
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Character-Id, X-Character-Name, X-Character-Role")
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
    """Get current student ID from character header or create/get student from character info."""
    try:
        # Get character info from header
        character_id = request.headers.get('X-Character-Id')
        character_name = request.headers.get('X-Character-Name', '')
        character_role = request.headers.get('X-Character-Role', 'student')
        
        if not character_id:
            return None
        
        db = SessionLocal()
        try:
            # Try to find existing student by character_id (stored in a custom field or use id mapping)
            # For simplicity, we'll use character_id as a string identifier
            # In a real implementation, you might want to store character_id in the Student model
            # For now, we'll create/get a student based on character_id
            student = db.query(Student).filter(Student.email == f"{character_id}@character.local").first()
            
            if not student:
                # Create a new student record for this character
                student = Student(
                    email=f"{character_id}@character.local",
                    name=character_name or "Character",
                    password_hash="no-auth"  # No password needed
                )
                db.add(student)
                db.commit()
                db.refresh(student)
            
            return student.id
        finally:
            db.close()
    except Exception as e:
        app.logger.error(f"Error getting current student ID: {str(e)}\n{traceback.format_exc()}")
        return None

@app.route("/api/character", methods=["GET"])
def get_current_character():
    """Get current character info from headers."""
    try:
        character_id = request.headers.get('X-Character-Id')
        character_name = request.headers.get('X-Character-Name', '')
        character_role = request.headers.get('X-Character-Role', 'student')
        
        if not character_id:
            return jsonify({"error": "Character not configured"}), 400
        
        return jsonify({
            "id": character_id,
            "name": character_name,
            "role": character_role
        })
    except Exception as e:
        app.logger.error(f"Get current character error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/materials", methods=["GET"])
def get_materials():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Character not configured"}), 400
    
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
        return jsonify({"error": "Character not configured"}), 400
    
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
        return jsonify({"error": "Character not configured"}), 400
    
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
        return jsonify({"error": "Character not configured"}), 400
    
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
        return jsonify({"error": "Character not configured"}), 400
    
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
        return jsonify({"error": "Character not configured"}), 400
    
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
        return jsonify({"error": "Character not configured"}), 400
    
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
        return jsonify({"error": "Character not configured"}), 400
    
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
        return jsonify({"error": "Character not configured"}), 400
    
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
        return jsonify({"error": "Character not configured"}), 400
    
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
        return jsonify({"error": "Character not configured"}), 400
    
    db = SessionLocal()
    try:
        from sqlalchemy import func
        
        # Total materials
        total_materials = db.query(func.count(Material.id)).scalar() or 0
        
        # Total bookmarks
        total_bookmarks = db.query(func.count(Bookmark.id)).filter(Bookmark.student_id == student_id).scalar() or 0
        
        # Progress stats
        completed_count = db.query(Progress).filter(
            Progress.student_id == student_id,
            Progress.status == "completed"
        ).count()
        
        in_progress_count = db.query(Progress).filter(
            Progress.student_id == student_id,
            Progress.status == "in_progress"
        ).count()
        
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
        return jsonify({"error": "Character not configured"}), 400
    
    db = SessionLocal()
    try:
        from sqlalchemy import distinct
        categories = db.query(distinct(Material.category)).filter(Material.category.isnot(None)).all()
        return jsonify([cat[0] for cat in categories if cat[0]])
    finally:
        db.close()

# Study Sessions endpoints
@app.route("/api/sessions", methods=["GET"])
def get_sessions():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Character not configured"}), 400
    
    db = SessionLocal()
    try:
        sessions = db.query(StudySession).filter(
            StudySession.student_id == student_id
        ).order_by(StudySession.started_at.desc()).limit(50).all()
        
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
        return jsonify({"error": "Character not configured"}), 400
    
    data = request.json
    material_id = data.get("material_id")
    duration_minutes = data.get("duration_minutes", 0.0)
    notes = data.get("notes")
    started_at_str = data.get("started_at")
    ended_at_str = data.get("ended_at")
    
    from datetime import datetime
    
    db = SessionLocal()
    try:
        # Validate material if provided
        if material_id:
            material = db.query(Material).filter(Material.id == material_id).first()
            if not material:
                return jsonify({"error": "Material not found"}), 404
        
        # Parse dates
        started_at = datetime.fromisoformat(started_at_str.replace('Z', '+00:00')) if started_at_str else datetime.utcnow()
        ended_at = datetime.fromisoformat(ended_at_str.replace('Z', '+00:00')) if ended_at_str else datetime.utcnow()
        
        session = StudySession(
            student_id=student_id,
            material_id=material_id,
            duration_minutes=duration_minutes,
            notes=notes,
            started_at=started_at,
            ended_at=ended_at
        )
        db.add(session)
        db.commit()
        
        # Update study streak
        update_study_streak(db, student_id)
        
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

@app.route("/api/sessions/<int:session_id>", methods=["PUT"])
def update_session(session_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Character not configured"}), 400
    
    data = request.json
    db = SessionLocal()
    try:
        session = db.query(StudySession).filter(
            StudySession.id == session_id,
            StudySession.student_id == student_id
        ).first()
        
        if not session:
            return jsonify({"error": "Session not found"}), 404
        
        if "duration_minutes" in data:
            session.duration_minutes = data["duration_minutes"]
        if "notes" in data:
            session.notes = data["notes"]
        if "ended_at" in data:
            from datetime import datetime
            if data["ended_at"]:
                try:
                    session.ended_at = datetime.fromisoformat(data["ended_at"].replace("Z", "+00:00"))
                except:
                    pass
            else:
                session.ended_at = None
        
        db.commit()
        
        # Update study streak
        update_study_streak(db, student_id)
        
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

@app.route("/api/sessions/<int:session_id>", methods=["DELETE"])
def delete_session_endpoint(session_id):
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Character not configured"}), 400
    
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

# Alias for study-sessions
@app.route("/api/study-sessions", methods=["GET"])
def get_study_sessions_alias():
    return get_sessions()

@app.route("/api/study-sessions", methods=["POST"])
def create_study_sessions_alias():
    return create_session()

@app.route("/api/study-sessions/<int:session_id>", methods=["PUT"])
def update_study_sessions_alias(session_id):
    return update_session(session_id)

@app.route("/api/study-sessions/<int:session_id>", methods=["DELETE"])
def delete_study_sessions_alias(session_id):
    return delete_session_endpoint(session_id)

# Study Streak endpoints
def update_study_streak(db, student_id):
    """Update study streak for a student based on their study sessions."""
    from datetime import datetime, timedelta
    
    # Get or create streak record
    streak = db.query(StudyStreak).filter(StudyStreak.student_id == student_id).first()
    if not streak:
        streak = StudyStreak(student_id=student_id)
        db.add(streak)
    
    # Get today's date (UTC)
    today = datetime.utcnow().date()
    
    # Get last study date
    last_study_date = streak.last_study_date.date() if streak.last_study_date else None
    
    if last_study_date:
        days_diff = (today - last_study_date).days
        
        if days_diff == 0:
            # Already studied today, no change
            pass
        elif days_diff == 1:
            # Consecutive day, increment streak
            streak.current_streak_days += 1
            streak.longest_streak_days = max(streak.longest_streak_days, streak.current_streak_days)
        else:
            # Streak broken, reset to 1
            streak.current_streak_days = 1
    else:
        # First study session
        streak.current_streak_days = 1
        streak.longest_streak_days = 1
    
    streak.last_study_date = datetime.utcnow()
    db.commit()

@app.route("/api/streak", methods=["GET"])
def get_streak():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Character not configured"}), 400
    
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
            "current_streak": streak.current_streak_days,
            "longest_streak": streak.longest_streak_days,
            "last_study_date": streak.last_study_date.isoformat() if streak.last_study_date else None
        })
    finally:
        db.close()

# Analytics endpoint
@app.route("/api/analytics", methods=["GET"])
def get_analytics():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        from sqlalchemy import func
        from datetime import datetime, timedelta
        
        # Study time statistics
        total_study_time = db.query(func.sum(StudySession.duration_minutes)).filter(
            StudySession.student_id == student_id
        ).scalar() or 0.0
        
        # Study time this week
        week_ago = datetime.utcnow() - timedelta(days=7)
        study_time_this_week = db.query(func.sum(StudySession.duration_minutes)).filter(
            StudySession.student_id == student_id,
            StudySession.created_at >= week_ago
        ).scalar() or 0.0
        
        # Study time this month
        month_ago = datetime.utcnow() - timedelta(days=30)
        study_time_this_month = db.query(func.sum(StudySession.duration_minutes)).filter(
            StudySession.student_id == student_id,
            StudySession.created_at >= month_ago
        ).scalar() or 0.0
        
        # Total sessions
        total_sessions = db.query(StudySession).filter(StudySession.student_id == student_id).count()
        
        # Average session duration
        avg_session_duration = total_study_time / total_sessions if total_sessions > 0 else 0.0
        
        # Goals statistics
        total_goals = db.query(StudyGoal).filter(StudyGoal.student_id == student_id).count()
        completed_goals = db.query(StudyGoal).filter(
            StudyGoal.student_id == student_id,
            StudyGoal.completed == True
        ).count()
        
        # Notes statistics
        total_notes = db.query(Note).filter(Note.student_id == student_id).count()
        
        # Ratings statistics
        total_ratings = db.query(Rating).filter(Rating.student_id == student_id).count()
        avg_rating_given = db.query(func.avg(Rating.rating)).filter(
            Rating.student_id == student_id
        ).scalar() or 0.0
        
        # Most studied materials (top 5)
        top_materials = db.query(
            Material.id,
            Material.title,
            func.sum(StudySession.duration_minutes).label('total_time')
        ).join(
            StudySession, Material.id == StudySession.material_id
        ).filter(
            StudySession.student_id == student_id
        ).group_by(
            Material.id, Material.title
        ).order_by(
            func.sum(StudySession.duration_minutes).desc()
        ).limit(5).all()
        
        return jsonify({
            "study_time": {
                "total_minutes": round(total_study_time, 2),
                "total_hours": round(total_study_time / 60, 2),
                "this_week_minutes": round(study_time_this_week, 2),
                "this_month_minutes": round(study_time_this_month, 2),
                "total_sessions": total_sessions,
                "avg_session_duration": round(avg_session_duration, 2)
            },
            "goals": {
                "total": total_goals,
                "completed": completed_goals,
                "completion_rate": round((completed_goals / total_goals * 100) if total_goals > 0 else 0, 1)
            },
            "content": {
                "total_notes": total_notes,
                "total_ratings": total_ratings,
                "avg_rating_given": round(float(avg_rating_given), 1)
            },
            "top_materials": [{
                "id": m.id,
                "title": m.title,
                "total_time_minutes": round(m.total_time, 2)
            } for m in top_materials]
        })
    finally:
        db.close()

# Material recommendations endpoint
@app.route("/api/materials/recommendations", methods=["GET"])
def get_recommendations():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        # Get materials not yet started or in progress
        started_material_ids = {p.material_id for p in db.query(Progress).filter(
            Progress.student_id == student_id,
            Progress.status == "completed"
        ).all()}
        
        # Get bookmarked materials
        bookmarked_material_ids = {b.material_id for b in db.query(Bookmark).filter(
            Bookmark.student_id == student_id
        ).all()}
        
        # Recommend materials that are:
        # 1. Not completed
        # 2. Bookmarked (priority)
        # 3. In progress (priority)
        recommendations = []
        
        # Bookmarked and not completed
        bookmarked = db.query(Material).filter(
            Material.id.in_(bookmarked_material_ids),
            ~Material.id.in_(started_material_ids)
        ).limit(5).all()
        
        for m in bookmarked:
            recommendations.append({
                "id": m.id,
                "title": m.title,
                "category": m.category,
                "reason": "bookmarked"
            })
        
        # In progress materials
        in_progress = db.query(Material).join(Progress).filter(
            Progress.student_id == student_id,
            Progress.status == "in_progress"
        ).limit(5).all()
        
        for m in in_progress:
            if not any(r["id"] == m.id for r in recommendations):
                recommendations.append({
                    "id": m.id,
                    "title": m.title,
                    "category": m.category,
                    "reason": "in_progress"
                })
        
        # New materials not yet started
        if len(recommendations) < 10:
            new_materials = db.query(Material).filter(
                ~Material.id.in_(started_material_ids)
            ).order_by(Material.created_at.desc()).limit(10 - len(recommendations)).all()
            
            for m in new_materials:
                if not any(r["id"] == m.id for r in recommendations):
                    recommendations.append({
                        "id": m.id,
                        "title": m.title,
                        "category": m.category,
                        "reason": "new"
                    })
        
        return jsonify(recommendations[:10])
    finally:
        db.close()

# Notes endpoints
@app.route("/api/notes", methods=["GET"])
def get_notes():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Character not configured"}), 400
    
    material_id = request.args.get("material_id", type=int)
    
    db = SessionLocal()
    try:
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
        return jsonify({"error": "Character not configured"}), 400
    
    data = request.json
    material_id = data.get("material_id")
    content = data.get("content", "").strip()
    
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
            content=content
        )
        db.add(note)
        db.commit()
        
        return jsonify({
            "success": True,
            "note": {
                "id": note.id,
                "material_id": note.material_id,
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
        return jsonify({"error": "Character not configured"}), 400
    
    data = request.json
    content = data.get("content", "").strip()
    
    if not content:
        return jsonify({"error": "content is required"}), 400
    
    db = SessionLocal()
    try:
        note = db.query(Note).filter(
            Note.id == note_id,
            Note.student_id == student_id
        ).first()
        
        if not note:
            return jsonify({"error": "Note not found"}), 404
        
        note.content = content
        db.commit()
        
        return jsonify({
            "success": True,
            "note": {
                "id": note.id,
                "material_id": note.material_id,
                "content": note.content,
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
        return jsonify({"error": "Character not configured"}), 400
    
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
        return jsonify({"error": "Character not configured"}), 400
    
    material_id = request.args.get("material_id", type=int)
    
    db = SessionLocal()
    try:
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

@app.route("/api/ratings/material/<int:material_id>", methods=["GET"])
def get_material_ratings(material_id):
    """Get all ratings for a specific material (for average rating calculation)"""
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Character not configured"}), 400
    
    db = SessionLocal()
    try:
        from sqlalchemy import func
        
        # Get all ratings for this material
        ratings = db.query(Rating).filter(Rating.material_id == material_id).all()
        
        # Get current student's rating
        student_rating = db.query(Rating).filter(
            Rating.material_id == material_id,
            Rating.student_id == student_id
        ).first()
        
        # Calculate average
        avg_rating = db.query(func.avg(Rating.rating)).filter(
            Rating.material_id == material_id
        ).scalar() or 0.0
        
        return jsonify({
            "average_rating": round(float(avg_rating), 1),
            "total_ratings": len(ratings),
            "my_rating": {
                "id": student_rating.id,
                "rating": student_rating.rating,
                "comment": student_rating.comment
            } if student_rating else None,
            "all_ratings": [{
                "id": r.id,
                "rating": r.rating,
                "comment": r.comment,
                "student": {
                    "id": r.student.id,
                    "name": r.student.name
                },
                "created_at": r.created_at.isoformat() if r.created_at else None
            } for r in ratings]
        })
    finally:
        db.close()

@app.route("/api/ratings", methods=["POST"])
def create_rating():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Character not configured"}), 400
    
    data = request.json
    material_id = data.get("material_id")
    rating_value = data.get("rating")
    comment = data.get("comment", "").strip()
    
    if not material_id:
        return jsonify({"error": "material_id is required"}), 400
    if not rating_value or not isinstance(rating_value, int) or rating_value < 1 or rating_value > 5:
        return jsonify({"error": "rating must be an integer between 1 and 5"}), 400
    
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
            # Update existing rating
            existing.rating = rating_value
            existing.comment = comment if comment else existing.comment
            db.commit()
            
            return jsonify({
                "success": True,
                "rating": {
                    "id": existing.id,
                    "material_id": existing.material_id,
                    "rating": existing.rating,
                    "comment": existing.comment,
                    "updated_at": existing.updated_at.isoformat() if existing.updated_at else None
                }
            })
        else:
            # Create new rating
            rating = Rating(
                student_id=student_id,
                material_id=material_id,
                rating=rating_value,
                comment=comment if comment else None
            )
            db.add(rating)
            db.commit()
            
            return jsonify({
                "success": True,
                "rating": {
                    "id": rating.id,
                    "material_id": rating.material_id,
                    "rating": rating.rating,
                    "comment": rating.comment,
                    "created_at": rating.created_at.isoformat() if rating.created_at else None
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
        return jsonify({"error": "Character not configured"}), 400
    
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

# Study Goals endpoints
@app.route("/api/goals", methods=["GET"])
def get_goals():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Character not configured"}), 400
    
    completed = request.args.get("completed", type=str)
    
    db = SessionLocal()
    try:
        query = db.query(StudyGoal).filter(StudyGoal.student_id == student_id)
        
        if completed is not None:
            if completed.lower() == "true":
                query = query.filter(StudyGoal.completed == True)
            elif completed.lower() == "false":
                query = query.filter(StudyGoal.completed == False)
        
        goals = query.order_by(StudyGoal.created_at.desc()).all()
        
        return jsonify([{
            "id": g.id,
            "title": g.title,
            "description": g.description,
            "target_date": g.target_date.isoformat() if g.target_date else None,
            "material_id": g.material_id,
            "material": {
                "id": g.material.id,
                "title": g.material.title,
                "category": g.material.category
            } if g.material else None,
            "target_minutes": g.target_minutes,
            "completed": g.completed,
            "completed_at": g.completed_at.isoformat() if g.completed_at else None,
            "created_at": g.created_at.isoformat() if g.created_at else None,
            "updated_at": g.updated_at.isoformat() if g.updated_at else None
        } for g in goals])
    finally:
        db.close()

@app.route("/api/goals", methods=["POST"])
def create_goal():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Character not configured"}), 400
    
    data = request.json
    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    target_date_str = data.get("target_date")
    material_id = data.get("material_id")
    target_minutes = data.get("target_minutes")
    
    if not title:
        return jsonify({"error": "title is required"}), 400
    
    db = SessionLocal()
    try:
        # Validate material if provided
        if material_id:
            material = db.query(Material).filter(Material.id == material_id).first()
            if not material:
                return jsonify({"error": "Material not found"}), 404
        
        # Parse target date
        target_date = None
        if target_date_str:
            from datetime import datetime
            target_date = datetime.fromisoformat(target_date_str.replace('Z', '+00:00'))
        
        goal = StudyGoal(
            student_id=student_id,
            title=title,
            description=description if description else None,
            target_date=target_date,
            material_id=material_id,
            target_minutes=target_minutes
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
                "material_id": goal.material_id,
                "target_minutes": goal.target_minutes,
                "completed": goal.completed,
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
        return jsonify({"error": "Character not configured"}), 400
    
    data = request.json
    title = data.get("title")
    description = data.get("description")
    target_date_str = data.get("target_date")
    material_id = data.get("material_id")
    target_minutes = data.get("target_minutes")
    completed = data.get("completed")
    
    db = SessionLocal()
    try:
        goal = db.query(StudyGoal).filter(
            StudyGoal.id == goal_id,
            StudyGoal.student_id == student_id
        ).first()
        
        if not goal:
            return jsonify({"error": "Goal not found"}), 404
        
        # Update fields
        if title is not None:
            goal.title = title.strip()
        if description is not None:
            goal.description = description.strip() if description.strip() else None
        if target_date_str is not None:
            from datetime import datetime
            goal.target_date = datetime.fromisoformat(target_date_str.replace('Z', '+00:00')) if target_date_str else None
        if material_id is not None:
            if material_id:
                material = db.query(Material).filter(Material.id == material_id).first()
                if not material:
                    return jsonify({"error": "Material not found"}), 404
            goal.material_id = material_id
        if target_minutes is not None:
            goal.target_minutes = target_minutes
        if completed is not None:
            goal.completed = completed
            if completed and not goal.completed_at:
                from datetime import datetime
                goal.completed_at = datetime.utcnow()
            elif not completed:
                goal.completed_at = None
        
        db.commit()
        
        return jsonify({
            "success": True,
            "goal": {
                "id": goal.id,
                "title": goal.title,
                "description": goal.description,
                "target_date": goal.target_date.isoformat() if goal.target_date else None,
                "material_id": goal.material_id,
                "target_minutes": goal.target_minutes,
                "completed": goal.completed,
                "completed_at": goal.completed_at.isoformat() if goal.completed_at else None,
                "updated_at": goal.updated_at.isoformat() if goal.updated_at else None
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
        return jsonify({"error": "Character not configured"}), 400
    
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

# Convenience endpoints for MaterialDetail.vue
@app.route("/api/materials/<int:material_id>/notes", methods=["GET"])
def get_material_notes_endpoint(material_id):
    """Convenience endpoint matching MaterialDetail.vue expectations"""
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
            "material_id": n.material_id,
            "content": n.content,
            "created_at": n.created_at.isoformat() if n.created_at else None,
            "updated_at": n.updated_at.isoformat() if n.updated_at else None
        } for n in notes])
    finally:
        db.close()

@app.route("/api/materials/<int:material_id>/notes", methods=["POST"])
def create_material_note_endpoint(material_id):
    """Convenience endpoint matching MaterialDetail.vue expectations"""
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
        
        note = Note(
            student_id=student_id,
            material_id=material_id,
            content=content
        )
        db.add(note)
        db.commit()
        
        return jsonify({
            "success": True,
            "note": {
                "id": note.id,
                "material_id": note.material_id,
                "content": note.content,
                "created_at": note.created_at.isoformat() if note.created_at else None
            }
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/materials/<int:material_id>/ratings", methods=["GET"])
def get_material_ratings_endpoint(material_id):
    """Convenience endpoint matching MaterialDetail.vue expectations"""
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        # Get user's rating
        user_rating = db.query(Rating).filter(
            Rating.student_id == student_id,
            Rating.material_id == material_id
        ).first()
        
        return jsonify({
            "user_rating": {
                "id": user_rating.id,
                "rating": user_rating.rating,
                "comment": user_rating.comment,
                "created_at": user_rating.created_at.isoformat() if user_rating.created_at else None
            } if user_rating else None
        })
    finally:
        db.close()

@app.route("/api/materials/<int:material_id>/ratings", methods=["POST"])
def create_material_rating_endpoint(material_id):
    """Convenience endpoint matching MaterialDetail.vue expectations"""
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json
    rating_value = data.get("rating")
    comment = data.get("comment", "").strip()
    
    if not rating_value or not isinstance(rating_value, int) or rating_value < 1 or rating_value > 5:
        return jsonify({"error": "Rating must be between 1 and 5"}), 400
    
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
        
        from datetime import datetime
        if existing:
            # Update existing rating
            existing.rating = rating_value
            existing.comment = comment if comment else None
            existing.updated_at = datetime.utcnow()
            rating = existing
        else:
            # Create new rating
            rating = Rating(
                student_id=student_id,
                material_id=material_id,
                rating=rating_value,
                comment=comment if comment else None
            )
            db.add(rating)
        
        db.commit()
        
        return jsonify({
            "success": True,
            "rating": {
                "id": rating.id,
                "material_id": rating.material_id,
                "rating": rating.rating,
                "comment": rating.comment,
                "created_at": rating.created_at.isoformat() if rating.created_at else None
            }
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/materials/<int:material_id>/ratings", methods=["DELETE"])
def delete_material_rating_endpoint(material_id):
    """Convenience endpoint matching MaterialDetail.vue expectations"""
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        rating = db.query(Rating).filter(
            Rating.student_id == student_id,
            Rating.material_id == material_id
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

if __name__ == "__main__":
    app.run(debug=True, port=5000)
