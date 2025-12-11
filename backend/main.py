from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
import traceback
from datetime import datetime

from backend.database import engine, SessionLocal, Base
from backend.models import Material, Problem
from backend.services import pair_programming
from backend.services.notion_sync import notion_service
from backend.services.tutor import tutor_service

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

# Initialize SocketIO with CORS support
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5173", "http://localhost:5000", "http://127.0.0.1:5173"], async_mode='threading')

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

# Notion sync endpoint
@app.route("/api/materials/sync-notion", methods=["POST"])
def sync_notion():
    """Sync materials from Notion database"""
    import asyncio
    db = SessionLocal()
    try:
        # Run async sync in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(notion_service.sync_to_database(db))
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Notion sync error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e), "success": False}), 500
    finally:
        db.close()

# Problems API endpoints
@app.route("/api/problems", methods=["GET"])
def get_problems():
    """Get all problems - no authentication required"""
    db = SessionLocal()
    try:
        query = db.query(Problem)
        
        # Search functionality
        search = request.args.get("search", "").strip()
        if search:
            query = query.filter(
                (Problem.title.ilike(f"%{search}%")) |
                (Problem.description.ilike(f"%{search}%")) |
                (Problem.full_description.ilike(f"%{search}%"))
            )
        
        # Difficulty filter
        difficulty = request.args.get("difficulty", "").strip()
        if difficulty:
            query = query.filter(Problem.difficulty == difficulty)
        
        # Topic/tag filter
        topic = request.args.get("topic", "").strip()
        if topic:
            # Filter by JSON array containing the topic
            query = query.filter(Problem.tags.contains([topic]))
        
        # Category filter
        category = request.args.get("category", "").strip()
        if category:
            query = query.filter(Problem.category == category)
        
        problems = query.order_by(Problem.order_index, Problem.created_at).all()
        
        return jsonify([{
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "fullDescription": p.full_description,
            "difficulty": p.difficulty,
            "tags": p.tags or [],
            "points": p.points,
            "estimatedTime": p.estimated_time,
            "examples": p.examples or [],
            "constraints": p.constraints or [],
            "testCases": p.test_cases or [],
            "starterCode": p.starter_code,
            "category": p.category,
            "created_at": p.created_at.isoformat() if p.created_at else None
        } for p in problems])
    finally:
        db.close()

@app.route("/api/problems/<int:problem_id>", methods=["GET"])
def get_problem(problem_id):
    """Get a specific problem - no authentication required"""
    db = SessionLocal()
    try:
        problem = db.query(Problem).filter(Problem.id == problem_id).first()
        if not problem:
            return jsonify({"error": "Problem not found"}), 404
        
        return jsonify({
            "id": problem.id,
            "title": problem.title,
            "description": problem.description,
            "fullDescription": problem.full_description,
            "difficulty": problem.difficulty,
            "tags": problem.tags or [],
            "points": problem.points,
            "estimatedTime": problem.estimated_time,
            "examples": problem.examples or [],
            "constraints": problem.constraints or [],
            "testCases": problem.test_cases or [],
            "starterCode": problem.starter_code,
            "category": problem.category,
            "created_at": problem.created_at.isoformat() if problem.created_at else None
        })
    finally:
        db.close()

@app.route("/api/problems/topics", methods=["GET"])
def get_problem_topics():
    """Get all unique topics/tags from problems - no authentication required"""
    db = SessionLocal()
    try:
        problems = db.query(Problem).all()
        topics = set()
        for problem in problems:
            if problem.tags:
                topics.update(problem.tags)
        return jsonify(sorted(list(topics)))
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

# Tutor API endpoints
@app.route("/api/tutor/ask", methods=["POST"])
def ask_tutor():
    """Ask the AI tutor a question about a programming language"""
    try:
        data = request.json or {}
        question = data.get("question", "").strip()
        language = data.get("language", "Python").strip()
        
        if not question:
            return jsonify({"error": "Question is required"}), 400
        
        if not language:
            return jsonify({"error": "Language is required"}), 400
        
        # Generate tutor response
        result = tutor_service.create_tutor_response(question, language)
        
        if not result.get("success"):
            return jsonify({"error": result.get("error", "Failed to generate response")}), 500
        
        return jsonify({
            "success": True,
            "session_id": result["session_id"],
            "markdown": result["markdown"]
        })
    except Exception as e:
        app.logger.error(f"Tutor ask error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/tutor/feedback", methods=["POST"])
def tutor_feedback():
    """Provide feedback (like/dislike) and delete the markdown file"""
    try:
        data = request.json or {}
        session_id = data.get("session_id", "").strip()
        feedback = data.get("feedback", "").strip()  # "like" or "dislike"
        
        if not session_id:
            return jsonify({"error": "Session ID is required"}), 400
        
        if feedback not in ["like", "dislike"]:
            return jsonify({"error": "Feedback must be 'like' or 'dislike'"}), 400
        
        # Delete the markdown file
        deleted = tutor_service.delete_tutor_file(session_id)
        
        return jsonify({
            "success": True,
            "deleted": deleted,
            "message": "Thank you for your feedback!"
        })
    except Exception as e:
        app.logger.error(f"Tutor feedback error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

# Pair Programming API Endpoints
@app.route("/api/pair-programming/create", methods=["POST"])
def create_pair_session():
    """Create a new pair programming session"""
    try:
        data = request.json or {}
        host_user_id = data.get("user_id")
        host_username = data.get("username", "Host")
        
        session_id = pair_programming.create_session(host_user_id, host_username)
        session = pair_programming.get_session(session_id)
        
        return jsonify({
            "success": True,
            "session_id": session_id,
            "session": {
                "code": session["code"],
                "output": session["output"],
                "host_username": session["host_username"],
                "participants": session["participants"]
            }
        })
    except Exception as e:
        app.logger.error(f"Create session error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/pair-programming/<session_id>", methods=["GET"])
def get_pair_session(session_id):
    """Get pair programming session data"""
    try:
        session = pair_programming.get_session(session_id)
        if not session:
            return jsonify({"error": "Session not found"}), 404
        
        return jsonify({
            "success": True,
            "session": {
                "code": session["code"],
                "output": session["output"],
                "host_username": session["host_username"],
                "participants": session["participants"],
                "created_at": session["created_at"].isoformat() if session.get("created_at") else None,
                "expires_at": session["expires_at"].isoformat() if session.get("expires_at") else None
            }
        })
    except Exception as e:
        app.logger.error(f"Get session error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/pair-programming/<session_id>/extend", methods=["POST"])
def extend_pair_session(session_id):
    """Extend pair programming session expiration"""
    try:
        data = request.json or {}
        hours = data.get("hours", 24)
        
        success = pair_programming.extend_session(session_id, hours)
        if not success:
            return jsonify({"error": "Session not found"}), 404
        
        return jsonify({
            "success": True,
            "message": f"Session extended by {hours} hours"
        })
    except Exception as e:
        app.logger.error(f"Extend session error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

# WebSocket Events for Pair Programming
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to pair programming server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    pass

@socketio.on('join_session')
def handle_join_session(data):
    """Join a pair programming session"""
    try:
        session_id = data.get('session_id')
        user_id = data.get('user_id')
        username = data.get('username', 'Anonymous')
        
        if not session_id:
            emit('error', {'message': 'Session ID required'})
            return
        
        session = pair_programming.get_session(session_id)
        if not session:
            emit('error', {'message': 'Session not found'})
            return
        
        # Add participant
        success = pair_programming.add_participant(session_id, user_id, username, request.sid)
        if success:
            join_room(session_id)
            
            # Send current session state
            session = pair_programming.get_session(session_id)
            emit('session_state', {
                'code': session['code'],
                'output': session['output'],
                'participants': session['participants'],
                'messages': session.get('messages', [])[-50:],  # Last 50 messages
                'cursors': session.get('cursors', {}),
                'selections': session.get('selections', {})
            })
            
            # Notify others
            emit('participant_joined', {
                'username': username,
                'participants': session['participants']
            }, room=session_id, include_self=False)
        else:
            emit('error', {'message': 'Failed to join session'})
    except Exception as e:
        app.logger.error(f"Join session error: {str(e)}\n{traceback.format_exc()}")
        emit('error', {'message': str(e)})

@socketio.on('leave_session')
def handle_leave_session(data):
    """Leave a pair programming session"""
    try:
        session_id = data.get('session_id')
        if session_id:
            pair_programming.remove_participant(session_id, request.sid)
            leave_room(session_id)
            
            # Notify others
            session = pair_programming.get_session(session_id)
            if session:
                emit('participant_left', {
                    'participants': session['participants']
                }, room=session_id, include_self=False)
    except Exception as e:
        app.logger.error(f"Leave session error: {str(e)}\n{traceback.format_exc()}")

@socketio.on('code_change')
def handle_code_change(data):
    """Handle code changes from clients"""
    try:
        session_id = data.get('session_id')
        code = data.get('code')
        
        if not session_id or code is None:
            return
        
        # Update session code
        pair_programming.update_session_code(session_id, code)
        
        # Broadcast to all participants except sender
        emit('code_updated', {
            'code': code,
            'from': data.get('username', 'Anonymous')
        }, room=session_id, include_self=False)
    except Exception as e:
        app.logger.error(f"Code change error: {str(e)}\n{traceback.format_exc()}")

@socketio.on('output_change')
def handle_output_change(data):
    """Handle output changes from code execution"""
    try:
        session_id = data.get('session_id')
        output = data.get('output')
        
        if not session_id or output is None:
            return
        
        # Update session output
        pair_programming.update_session_output(session_id, output)
        
        # Broadcast to all participants
        emit('output_updated', {
            'output': output
        }, room=session_id)
    except Exception as e:
        app.logger.error(f"Output change error: {str(e)}\n{traceback.format_exc()}")

@socketio.on('cursor_change')
def handle_cursor_change(data):
    """Handle cursor position changes"""
    try:
        session_id = data.get('session_id')
        position = data.get('position')
        if session_id and position:
            # Update cursor in session
            pair_programming.update_cursor(session_id, request.sid, position)
            
            # Get username from participants
            session = pair_programming.get_session(session_id)
            username = 'Anonymous'
            if session:
                for p in session.get('participants', []):
                    if p.get('socket_id') == request.sid:
                        username = p.get('username', 'Anonymous')
                        break
            
            # Broadcast cursor position to others
            emit('cursor_updated', {
                'position': position,
                'username': username,
                'socket_id': request.sid
            }, room=session_id, include_self=False)
    except Exception as e:
        app.logger.error(f"Cursor change error: {str(e)}\n{traceback.format_exc()}")

@socketio.on('selection_change')
def handle_selection_change(data):
    """Handle code selection changes"""
    try:
        session_id = data.get('session_id')
        selection = data.get('selection')
        if session_id:
            # Update selection in session
            pair_programming.update_selection(session_id, request.sid, selection)
            
            # Get username from participants
            session = pair_programming.get_session(session_id)
            username = 'Anonymous'
            if session:
                for p in session.get('participants', []):
                    if p.get('socket_id') == request.sid:
                        username = p.get('username', 'Anonymous')
                        break
            
            # Broadcast selection to others
            emit('selection_updated', {
                'selection': selection,
                'username': username,
                'socket_id': request.sid
            }, room=session_id, include_self=False)
    except Exception as e:
        app.logger.error(f"Selection change error: {str(e)}\n{traceback.format_exc()}")

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle chat messages"""
    try:
        session_id = data.get('session_id')
        message = data.get('message', '').strip()
        username = data.get('username', 'Anonymous')
        
        if not session_id or not message:
            return
        
        # Broadcast chat message to all participants
        emit('chat_message', {
            'id': f"{session_id}-{int(__import__('time').time() * 1000)}",
            'username': username,
            'message': message,
            'timestamp': data.get('timestamp', __import__('datetime').datetime.now().isoformat())
        }, room=session_id)
    except Exception as e:
        app.logger.error(f"Chat message error: {str(e)}\n{traceback.format_exc()}")

@socketio.on('typing_start')
def handle_typing_start(data):
    """Handle typing start indicator"""
    try:
        session_id = data.get('session_id')
        if session_id:
            emit('typing_start', {
                'username': data.get('username', 'Anonymous')
            }, room=session_id, include_self=False)
    except Exception as e:
        app.logger.error(f"Typing start error: {str(e)}\n{traceback.format_exc()}")

@socketio.on('typing_stop')
def handle_typing_stop(data):
    """Handle typing stop indicator"""
    try:
        session_id = data.get('session_id')
        if session_id:
            emit('typing_stop', {
                'username': data.get('username', 'Anonymous')
            }, room=session_id, include_self=False)
    except Exception as e:
        app.logger.error(f"Typing stop error: {str(e)}\n{traceback.format_exc()}")

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)
