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
     origins=["http://localhost:5173", "http://localhost:5001", "http://127.0.0.1:5173"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     expose_headers=["Content-Type"])

# Initialize SocketIO with CORS support
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5173", "http://localhost:5001", "http://127.0.0.1:5173"], async_mode='threading')

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
    # #region agent log
    log_path = '/Users/nenadkalicanin/Documents/Github/december/December-Vue-StudyHall/.cursor/debug.log'
    try:
        import json, os, time
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'a') as f:
            f.write(json.dumps({"location":"main.py:get_materials","message":"Function entry","data":{"args":dict(request.args)},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"post-fix","hypothesisId":"B"})+'\n')
    except:
        pass  # Don't let logging break the endpoint
    # #endregion
    
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
        
        # #region agent log
        try:
            with open(log_path, 'a') as f:
                f.write(json.dumps({"location":"main.py:get_materials","message":"Query successful","data":{"count":len(materials)},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"post-fix","hypothesisId":"B"})+'\n')
        except:
            pass
        # #endregion
        
        return jsonify([{
            "id": m.id,
            "title": m.title,
            "content": m.content,
            "category": m.category,
            "notion_url": m.notion_url,
            "created_at": m.created_at.isoformat() if m.created_at else None
        } for m in materials])
    except Exception as e:
        # #region agent log
        try:
            error_msg = str(e)
            error_tb = traceback.format_exc()
            with open(log_path, 'a') as f:
                f.write(json.dumps({"location":"main.py:get_materials","message":"Error occurred","data":{"error":error_msg,"traceback":error_tb},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"post-fix","hypothesisId":"B"})+'\n')
        except:
            pass
        # #endregion
        app.logger.error(f"Get materials error: {str(e)}\n{traceback.format_exc()}")
        print(f"ERROR in get_materials: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500
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
    # #region agent log
    log_path = '/Users/nenadkalicanin/Documents/Github/december/December-Vue-StudyHall/.cursor/debug.log'
    print("[DEBUG] get_categories called")  # Force console output
    try:
        import json, os, time
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'a') as f:
            f.write(json.dumps({"location":"main.py:get_categories","message":"Function entry","timestamp":time.time()*1000,"sessionId":"debug-session","runId":"post-fix","hypothesisId":"B"})+'\n')
    except Exception as log_err:
        print(f"[DEBUG] Logging failed: {log_err}")  # Show if logging fails
    # #endregion
    
    db = SessionLocal()
    try:
        print("[DEBUG] Querying categories...")  # Force console output
        
        # Fix: Use correct SQLAlchemy syntax for distinct query
        # Query distinct categories directly using .distinct() method
        categories = db.query(Material.category).filter(Material.category.isnot(None)).distinct().all()
        
        print(f"[DEBUG] Found {len(categories)} categories")  # Force console output
        
        # #region agent log
        try:
            with open(log_path, 'a') as f:
                f.write(json.dumps({"location":"main.py:get_categories","message":"Query successful","data":{"raw_categories":str(categories),"count":len(categories)},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"post-fix","hypothesisId":"B"})+'\n')
        except:
            pass
        # #endregion
        
        # Extract category strings from Row objects
        # SQLAlchemy returns Row objects which can be indexed like tuples: Row('Python',)
        # Simply access the first element: cat[0]
        result = [cat[0] for cat in categories if cat[0]]
        
        print(f"[DEBUG] Returning {len(result)} categories: {result}")  # Force console output
        return jsonify(result)
    except Exception as e:
        # #region agent log
        error_msg = str(e)
        error_tb = traceback.format_exc()
        print(f"[DEBUG] ERROR in get_categories: {error_msg}")  # Force console output
        print(f"[DEBUG] Traceback: {error_tb}")  # Force console output
        try:
            with open(log_path, 'a') as f:
                f.write(json.dumps({"location":"main.py:get_categories","message":"Error occurred","data":{"error":error_msg,"traceback":error_tb},"timestamp":time.time()*1000,"sessionId":"debug-session","runId":"post-fix","hypothesisId":"B"})+'\n')
        except:
            pass
        # #endregion
        app.logger.error(f"Get categories error: {error_msg}\n{error_tb}")
        return jsonify({"error": error_msg, "traceback": error_tb}), 500
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

# Global Search endpoint - searches across all content types
@app.route("/api/search", methods=["GET"])
def global_search():
    """Search across materials, problems, and other content - no authentication required"""
    db = SessionLocal()
    try:
        query = request.args.get("q", "").strip()
        content_types = request.args.get("types", "materials,problems").split(",")
        
        if not query:
            return jsonify({"results": []})
        
        results = []
        search_lower = query.lower()
        
        # Search materials
        if "materials" in content_types:
            materials = db.query(Material).filter(
                (Material.title.ilike(f"%{query}%")) |
                (Material.content.ilike(f"%{query}%"))
            ).limit(20).all()
            
            for m in materials:
                results.append({
                    "id": m.id,
                    "title": m.title,
                    "description": (m.content or "")[:200],
                    "type": "materials",
                    "category": m.category,
                    "route": f"/materials/{m.id}"
                })
        
        # Search problems
        if "problems" in content_types:
            problems = db.query(Problem).filter(
                (Problem.title.ilike(f"%{query}%")) |
                (Problem.description.ilike(f"%{query}%")) |
                (Problem.full_description.ilike(f"%{query}%"))
            ).limit(20).all()
            
            for p in problems:
                results.append({
                    "id": p.id,
                    "title": p.title,
                    "description": (p.description or "")[:200],
                    "type": "problems",
                    "category": p.category or "General",
                    "route": f"/practice-problems"
                })
        
        return jsonify({"results": results})
    except Exception as e:
        app.logger.error(f"Global search error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e), "results": []}), 500
    finally:
        db.close()

# Snippets API endpoints
@app.route("/api/snippets", methods=["GET"])
def get_snippets():
    """Get code snippets - no authentication required"""
    # For MVP, return static snippets. Can be moved to database later
    snippets = [
        {
            "id": 1,
            "name": "Hello World",
            "category": "Basics",
            "description": "Basic print statement",
            "code": 'print("Hello, World!")'
        },
        {
            "id": 2,
            "name": "Variables and Types",
            "category": "Basics",
            "description": "Variable assignment and type checking",
            "code": "# Variable assignment\nname = 'StudyHall'\nage = 25\nis_active = True\n\n# Type checking\nprint(type(name))  # <class 'str'>\nprint(type(age))   # <class 'int'>"
        },
        {
            "id": 3,
            "name": "Lists Operations",
            "category": "Data Structures",
            "description": "Common list operations",
            "code": "# List operations\nnumbers = [1, 2, 3, 4, 5]\n\n# Access elements\nprint(numbers[0])      # 1\nprint(numbers[-1])     # 5\n\n# Slice\nprint(numbers[1:3])    # [2, 3]\n\n# Modify\nnumbers.append(6)     # [1, 2, 3, 4, 5, 6]\nnumbers.insert(0, 0)   # [0, 1, 2, 3, 4, 5, 6]"
        },
        {
            "id": 4,
            "name": "For Loops",
            "category": "Control Flow",
            "description": "Iterating with for loops",
            "code": "# For loop examples\n\n# Iterate over list\nfruits = ['apple', 'banana', 'orange']\nfor fruit in fruits:\n    print(fruit)\n\n# With range\nfor i in range(5):\n    print(i)  # 0, 1, 2, 3, 4\n\n# With enumerate\nfor index, fruit in enumerate(fruits):\n    print(f'{index}: {fruit}')"
        },
        {
            "id": 5,
            "name": "Functions",
            "category": "Functions",
            "description": "Define and call functions",
            "code": "# Function definition\ndef greet(name):\n    return f'Hello, {name}!'\n\n# Function call\nmessage = greet('StudyHall')\nprint(message)  # Hello, StudyHall!\n\n# Function with default parameters\ndef power(base, exponent=2):\n    return base ** exponent\n\nprint(power(3))      # 9\nprint(power(3, 3))   # 27"
        },
        {
            "id": 6,
            "name": "Dictionaries",
            "category": "Data Structures",
            "description": "Key-value pairs",
            "code": "# Dictionary operations\nstudent = {\n    'name': 'Alice',\n    'age': 20,\n    'grade': 'A'\n}\n\n# Access values\nprint(student['name'])        # Alice\nprint(student.get('age'))     # 20\n\n# Add/Update\nstudent['email'] = 'alice@example.com'\nstudent['age'] = 21\n\n# Iterate\nfor key, value in student.items():\n    print(f'{key}: {value}')"
        }
    ]
    
    # Filter by search query if provided
    search = request.args.get("search", "").strip().lower()
    category = request.args.get("category", "").strip()
    
    filtered = snippets
    if search:
        filtered = [s for s in filtered if search in s["name"].lower() or search in s["description"].lower()]
    if category:
        filtered = [s for s in filtered if s["category"].lower() == category.lower()]
    
    return jsonify(filtered)

# Cheat Sheets API endpoints
@app.route("/api/cheat-sheets", methods=["GET"])
def get_cheat_sheets():
    """Get cheat sheets - no authentication required"""
    cheat_sheets = [
        {
            "id": 1,
            "title": "Python Basics",
            "description": "Essential Python syntax and operations",
            "sections": [
                {
                    "title": "Variables",
                    "content": "name = 'StudyHall'\nage = 25\nis_active = True"
                },
                {
                    "title": "Print",
                    "content": "print('Hello')\nprint(f'Age: {age}')"
                }
            ]
        },
        {
            "id": 2,
            "title": "Lists",
            "description": "List operations and methods",
            "sections": [
                {
                    "title": "Create",
                    "content": "numbers = [1, 2, 3]\nempty = []"
                },
                {
                    "title": "Methods",
                    "content": "numbers.append(4)\nnumbers.insert(0, 0)\nnumbers.remove(2)\nnumbers.pop()"
                }
            ]
        }
    ]
    
    search = request.args.get("search", "").strip().lower()
    if search:
        cheat_sheets = [cs for cs in cheat_sheets if search in cs["title"].lower() or search in cs["description"].lower()]
    
    return jsonify(cheat_sheets)

# Resources API endpoints
@app.route("/api/resources", methods=["GET"])
def get_resources():
    """Get learning resources - no authentication required"""
    resources = [
        {
            "id": 1,
            "title": "Python Official Documentation",
            "description": "Comprehensive official documentation for Python programming language.",
            "url": "https://docs.python.org/3/",
            "category": "Documentation",
            "type": "Official",
            "free": True
        },
        {
            "id": 2,
            "title": "Real Python",
            "description": "High-quality Python tutorials, articles, and courses for developers of all skill levels.",
            "url": "https://realpython.com/",
            "category": "Tutorials",
            "type": "Tutorial",
            "free": True
        },
        {
            "id": 3,
            "title": "Python.org Tutorial",
            "description": "Official Python tutorial covering basics to advanced topics. Perfect for beginners.",
            "url": "https://docs.python.org/3/tutorial/",
            "category": "Tutorials",
            "type": "Official",
            "free": True
        },
        {
            "id": 4,
            "title": "LeetCode",
            "description": "Practice coding problems and improve your problem-solving skills with Python.",
            "url": "https://leetcode.com/",
            "category": "Practice",
            "type": "Platform",
            "free": True
        }
    ]
    
    # Search functionality
    search = request.args.get("search", "").strip().lower()
    if search:
        resources = [r for r in resources if search in r["title"].lower() or search in r["description"].lower() or search in r["category"].lower()]
    
    # Category filter
    category = request.args.get("category", "").strip()
    if category and category != "All":
        resources = [r for r in resources if r["category"].lower() == category.lower()]
    
    return jsonify(resources)

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

# Tools API endpoints
@app.route("/api/tools/hash", methods=["POST"])
def generate_hash():
    """Generate hash (MD5, SHA1, SHA256) for text - no authentication required"""
    try:
        data = request.json or {}
        text = data.get("text", "").strip()
        algorithm = data.get("algorithm", "sha256").strip().lower()
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        import hashlib
        
        # Generate hash based on algorithm
        if algorithm == "md5":
            hash_obj = hashlib.md5(text.encode('utf-8'))
        elif algorithm == "sha1":
            hash_obj = hashlib.sha1(text.encode('utf-8'))
        elif algorithm == "sha256":
            hash_obj = hashlib.sha256(text.encode('utf-8'))
        else:
            return jsonify({"error": "Unsupported algorithm. Use md5, sha1, or sha256"}), 400
        
        hash_hex = hash_obj.hexdigest()
        
        return jsonify({
            "success": True,
            "algorithm": algorithm,
            "hash": hash_hex
        })
    except Exception as e:
        app.logger.error(f"Hash generation error: {str(e)}\n{traceback.format_exc()}")
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
        
        # Store message in session
        pair_programming.add_message(session_id, username, message, request.sid)
        
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
            # Update typing status in session
            pair_programming.set_typing(session_id, request.sid, True)
            
            # Get username from participants
            session = pair_programming.get_session(session_id)
            username = 'Anonymous'
            if session:
                for p in session.get('participants', []):
                    if p.get('socket_id') == request.sid:
                        username = p.get('username', 'Anonymous')
                        break
            
            emit('typing_start', {
                'username': username
            }, room=session_id, include_self=False)
    except Exception as e:
        app.logger.error(f"Typing start error: {str(e)}\n{traceback.format_exc()}")

@socketio.on('typing_stop')
def handle_typing_stop(data):
    """Handle typing stop indicator"""
    try:
        session_id = data.get('session_id')
        if session_id:
            # Update typing status in session
            pair_programming.set_typing(session_id, request.sid, False)
            
            # Get username from participants
            session = pair_programming.get_session(session_id)
            username = 'Anonymous'
            if session:
                for p in session.get('participants', []):
                    if p.get('socket_id') == request.sid:
                        username = p.get('username', 'Anonymous')
                        break
            
            emit('typing_stop', {
                'username': username
            }, room=session_id, include_self=False)
    except Exception as e:
        app.logger.error(f"Typing stop error: {str(e)}\n{traceback.format_exc()}")

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5001, allow_unsafe_werkzeug=True)
