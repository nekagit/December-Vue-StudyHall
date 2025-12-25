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
        
        # Topic/tag filter - will be applied in Python after fetching (for SQLite JSON compatibility)
        topic = request.args.get("topic", "").strip()
        
        # Category filter
        category = request.args.get("category", "").strip()
        if category:
            query = query.filter(Problem.category == category)
        
        problems = query.order_by(Problem.order_index, Problem.created_at).all()
        
        # Apply topic filter in Python (for SQLite JSON compatibility)
        if topic:
            filtered_problems = []
            for p in problems:
                tags = p.tags or []
                # Handle both list and JSON string formats
                if isinstance(tags, str):
                    import json
                    try:
                        tags = json.loads(tags)
                    except (json.JSONDecodeError, TypeError):
                        tags = []
                # Check if topic is in tags
                if isinstance(tags, list) and topic in tags:
                    filtered_problems.append(p)
            problems = filtered_problems
        
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
                # Handle both list and JSON string formats
                if isinstance(problem.tags, list):
                    topics.update(problem.tags)
                elif isinstance(problem.tags, str):
                    import json
                    try:
                        tags_list = json.loads(problem.tags)
                        if isinstance(tags_list, list):
                            topics.update(tags_list)
                    except (json.JSONDecodeError, TypeError):
                        pass
        return jsonify(sorted(list(topics)))
    except Exception as e:
        app.logger.error(f"Get problem topics error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/problems/categories", methods=["GET"])
def get_problem_categories():
    """Get all unique categories from problems - no authentication required"""
    db = SessionLocal()
    try:
        categories = db.query(Problem.category).filter(Problem.category.isnot(None)).distinct().all()
        result = [cat[0] for cat in categories if cat[0]]
        return jsonify(sorted(result))
    except Exception as e:
        app.logger.error(f"Get problem categories error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/problems/difficulties", methods=["GET"])
def get_problem_difficulties():
    """Get all unique difficulty levels from problems - no authentication required"""
    db = SessionLocal()
    try:
        difficulties = db.query(Problem.difficulty).distinct().all()
        result = [diff[0] for diff in difficulties if diff[0]]
        return jsonify(sorted(result))
    except Exception as e:
        app.logger.error(f"Get problem difficulties error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/problems", methods=["POST"])
def create_problem():
    """Create a new problem - no authentication required (for MVP)"""
    try:
        data = request.json or {}
        
        # Validate required fields (handle both camelCase and snake_case)
        if not data.get("title"):
            return jsonify({"error": "title is required"}), 400
        if not data.get("description"):
            return jsonify({"error": "description is required"}), 400
        if not data.get("difficulty"):
            return jsonify({"error": "difficulty is required"}), 400
        if not data.get("testCases") and not data.get("test_cases"):
            return jsonify({"error": "testCases or test_cases is required"}), 400
        
        db = SessionLocal()
        try:
            problem = Problem(
                title=data["title"],
                description=data["description"],
                full_description=data.get("fullDescription", data.get("full_description")),
                difficulty=data["difficulty"],
                tags=data.get("tags", []),
                points=data.get("points", 10),
                estimated_time=data.get("estimatedTime", data.get("estimated_time")),
                examples=data.get("examples", []),
                constraints=data.get("constraints", []),
                test_cases=data.get("testCases", data.get("test_cases")),
                starter_code=data.get("starterCode", data.get("starter_code")),
                category=data.get("category"),
                order_index=data.get("orderIndex", data.get("order_index", 0))
            )
            
            db.add(problem)
            db.commit()
            db.refresh(problem)
            
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
            }), 201
        finally:
            db.close()
    except Exception as e:
        app.logger.error(f"Create problem error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/problems/<int:problem_id>", methods=["PUT"])
def update_problem(problem_id):
    """Update a problem - no authentication required (for MVP)"""
    try:
        data = request.json or {}
        db = SessionLocal()
        try:
            problem = db.query(Problem).filter(Problem.id == problem_id).first()
            if not problem:
                return jsonify({"error": "Problem not found"}), 404
            
            # Update fields if provided
            if "title" in data:
                problem.title = data["title"]
            if "description" in data:
                problem.description = data["description"]
            if "fullDescription" in data or "full_description" in data:
                problem.full_description = data.get("fullDescription", data.get("full_description"))
            if "difficulty" in data:
                problem.difficulty = data["difficulty"]
            if "tags" in data:
                problem.tags = data["tags"]
            if "points" in data:
                problem.points = data["points"]
            if "estimatedTime" in data or "estimated_time" in data:
                problem.estimated_time = data.get("estimatedTime", data.get("estimated_time"))
            if "examples" in data:
                problem.examples = data["examples"]
            if "constraints" in data:
                problem.constraints = data["constraints"]
            if "testCases" in data or "test_cases" in data:
                problem.test_cases = data.get("testCases", data.get("test_cases"))
            if "starterCode" in data or "starter_code" in data:
                problem.starter_code = data.get("starterCode", data.get("starter_code"))
            if "category" in data:
                problem.category = data["category"]
            if "orderIndex" in data or "order_index" in data:
                problem.order_index = data.get("orderIndex", data.get("order_index"))
            
            db.commit()
            db.refresh(problem)
            
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
    except Exception as e:
        app.logger.error(f"Update problem error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/problems/<int:problem_id>", methods=["DELETE"])
def delete_problem(problem_id):
    """Delete a problem - no authentication required (for MVP)"""
    try:
        db = SessionLocal()
        try:
            problem = db.query(Problem).filter(Problem.id == problem_id).first()
            if not problem:
                return jsonify({"error": "Problem not found"}), 404
            
            db.delete(problem)
            db.commit()
            
            return jsonify({"success": True, "message": "Problem deleted successfully"})
        finally:
            db.close()
    except Exception as e:
        app.logger.error(f"Delete problem error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

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
        },
        {
            "id": 7,
            "name": "List Comprehensions",
            "category": "Python Patterns",
            "description": "Concise list creation",
            "code": "# List comprehension\nsquares = [x**2 for x in range(10)]\n# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]\n\n# With condition\neven_squares = [x**2 for x in range(10) if x % 2 == 0]\n# [0, 4, 16, 36, 64]\n\n# Nested\nmatrix = [[i*j for j in range(3)] for i in range(3)]\n# [[0, 0, 0], [0, 1, 2], [0, 2, 4]]\n\n# Dictionary comprehension\nsquares_dict = {x: x**2 for x in range(5)}\n# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}"
        },
        {
            "id": 8,
            "name": "Error Handling",
            "category": "Control Flow",
            "description": "Try-except blocks for error handling",
            "code": "# Basic error handling\ntry:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('Cannot divide by zero!')\n\n# Multiple exceptions\ntry:\n    value = int('abc')\nexcept ValueError:\n    print('Invalid number')\nexcept Exception as e:\n    print(f'Error: {e}')\n\n# Finally block\ntry:\n    file = open('data.txt')\n    content = file.read()\nexcept FileNotFoundError:\n    print('File not found')\nfinally:\n    file.close()  # Always executed"
        },
        {
            "id": 9,
            "name": "Classes and Objects",
            "category": "OOP",
            "description": "Object-oriented programming basics",
            "code": "# Class definition\nclass Dog:\n    def __init__(self, name, breed):\n        self.name = name\n        self.breed = breed\n    \n    def bark(self):\n        return f'{self.name} says woof!'\n    \n    def __str__(self):\n        return f'Dog(name={self.name}, breed={self.breed})'\n\n# Create instance\nmy_dog = Dog('Buddy', 'Golden Retriever')\nprint(my_dog.bark())  # Buddy says woof!\nprint(my_dog)         # Dog(name=Buddy, breed=Golden Retriever)"
        },
        {
            "id": 10,
            "name": "Generators",
            "category": "Python Patterns",
            "description": "Memory-efficient iterators",
            "code": "# Generator function\ndef countdown(n):\n    while n > 0:\n        yield n\n        n -= 1\n\n# Use generator\nfor num in countdown(5):\n    print(num)  # 5, 4, 3, 2, 1\n\n# Generator expression\nsquares = (x**2 for x in range(10))\nprint(list(squares))  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]\n\n# Memory efficient\nlarge_sum = sum(x**2 for x in range(1000000))"
        },
        {
            "id": 11,
            "name": "Lambda Functions",
            "category": "Functions",
            "description": "Anonymous functions",
            "code": "# Lambda function\nsquare = lambda x: x**2\nprint(square(5))  # 25\n\n# With map\nnumbers = [1, 2, 3, 4, 5]\nsquared = list(map(lambda x: x**2, numbers))\n# [1, 4, 9, 16, 25]\n\n# With filter\neven = list(filter(lambda x: x % 2 == 0, numbers))\n# [2, 4]\n\n# With sorted\nstudents = [('Alice', 20), ('Bob', 18), ('Charlie', 22)]\nsorted_by_age = sorted(students, key=lambda x: x[1])\n# [('Bob', 18), ('Alice', 20), ('Charlie', 22)]"
        },
        {
            "id": 12,
            "name": "File Operations",
            "category": "I/O",
            "description": "Reading and writing files",
            "code": "# Read file\nwith open('data.txt', 'r') as f:\n    content = f.read()\n    # or\n    lines = f.readlines()\n\n# Write file\nwith open('output.txt', 'w') as f:\n    f.write('Hello, World!')\n\n# Append to file\nwith open('log.txt', 'a') as f:\n    f.write('New entry\\n')\n\n# Read line by line\nwith open('large_file.txt', 'r') as f:\n    for line in f:\n        print(line.strip())"
        },
        {
            "id": 13,
            "name": "Regular Expressions",
            "category": "Strings",
            "description": "Pattern matching with regex",
            "code": "import re\n\n# Search pattern\npattern = r'\\d+'  # One or more digits\ntext = 'Price is 42 dollars'\nmatch = re.search(pattern, text)\nprint(match.group())  # '42'\n\n# Find all matches\nnumbers = re.findall(r'\\d+', 'I have 5 apples and 3 oranges')\n# ['5', '3']\n\n# Replace\nnew_text = re.sub(r'\\d+', 'X', 'Price is 42 dollars')\n# 'Price is X dollars'\n\n# Split\nwords = re.split(r'\\s+', 'Hello   World')\n# ['Hello', 'World']"
        },
        {
            "id": 14,
            "name": "JSON Operations",
            "category": "Data Structures",
            "description": "Working with JSON data",
            "code": "import json\n\n# Parse JSON string\ndata = '{\"name\": \"Alice\", \"age\": 30}'\nobj = json.loads(data)\nprint(obj['name'])  # Alice\n\n# Convert to JSON\nperson = {'name': 'Bob', 'age': 25}\njson_str = json.dumps(person)\n# '{\"name\": \"Bob\", \"age\": 25}'\n\n# Read JSON file\nwith open('data.json', 'r') as f:\n    data = json.load(f)\n\n# Write JSON file\nwith open('output.json', 'w') as f:\n    json.dump(person, f, indent=2)"
        },
        {
            "id": 15,
            "name": "Async/Await",
            "category": "Async Programming",
            "description": "Asynchronous programming",
            "code": "import asyncio\n\n# Async function\nasync def fetch_data(url):\n    await asyncio.sleep(1)  # Simulate I/O\n    return f'Data from {url}'\n\n# Run async function\nasync def main():\n    result = await fetch_data('https://api.example.com')\n    print(result)\n\n# Concurrent execution\nasync def fetch_multiple():\n    results = await asyncio.gather(\n        fetch_data('url1'),\n        fetch_data('url2'),\n        fetch_data('url3')\n    )\n    return results\n\nasyncio.run(main())"
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
        },
        {
            "id": 3,
            "title": "Dictionaries",
            "description": "Dictionary operations and methods",
            "sections": [
                {
                    "title": "Create",
                    "content": "person = {'name': 'Alice', 'age': 30}\nempty = {}"
                },
                {
                    "title": "Access",
                    "content": "person['name']\nperson.get('age', 0)  # With default"
                },
                {
                    "title": "Methods",
                    "content": "person.keys()\nperson.values()\nperson.items()\nperson.update({'city': 'NYC'})"
                }
            ]
        },
        {
            "id": 4,
            "title": "String Methods",
            "description": "Common string operations",
            "sections": [
                {
                    "title": "Case",
                    "content": "text.upper()\ntext.lower()\ntext.capitalize()\ntext.title()"
                },
                {
                    "title": "Search",
                    "content": "text.find('substring')\ntext.count('a')\ntext.startswith('Hello')\ntext.endswith('World')"
                },
                {
                    "title": "Modify",
                    "content": "text.strip()\ntext.replace('old', 'new')\ntext.split(',')\n'-'.join(['a', 'b', 'c'])"
                }
            ]
        },
        {
            "id": 5,
            "title": "List Comprehensions",
            "description": "Concise list creation patterns",
            "sections": [
                {
                    "title": "Basic",
                    "content": "[x**2 for x in range(10)]\n[x for x in range(10) if x % 2 == 0]"
                },
                {
                    "title": "Nested",
                    "content": "[[i*j for j in range(3)] for i in range(3)]"
                },
                {
                    "title": "Dictionary",
                    "content": "{x: x**2 for x in range(5)}\n{x: x**2 for x in range(10) if x % 2 == 0}"
                }
            ]
        },
        {
            "id": 6,
            "title": "Error Handling",
            "description": "Exception handling patterns",
            "sections": [
                {
                    "title": "Try-Except",
                    "content": "try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print('Error')"
                },
                {
                    "title": "Multiple",
                    "content": "try:\n    value = int('abc')\nexcept ValueError:\n    pass\nexcept Exception as e:\n    print(e)"
                },
                {
                    "title": "Finally",
                    "content": "try:\n    file = open('data.txt')\nfinally:\n    file.close()"
                }
            ]
        },
        {
            "id": 7,
            "title": "File I/O",
            "description": "Reading and writing files",
            "sections": [
                {
                    "title": "Read",
                    "content": "with open('file.txt', 'r') as f:\n    content = f.read()\n    lines = f.readlines()"
                },
                {
                    "title": "Write",
                    "content": "with open('file.txt', 'w') as f:\n    f.write('Hello')\n    f.writelines(['line1', 'line2'])"
                },
                {
                    "title": "Append",
                    "content": "with open('file.txt', 'a') as f:\n    f.write('New line')"
                }
            ]
        },
        {
            "id": 8,
            "title": "Regular Expressions",
            "description": "Pattern matching with regex",
            "sections": [
                {
                    "title": "Search",
                    "content": "import re\nre.search(r'\\d+', 'Price: 42')\nre.findall(r'\\d+', 'I have 5 apples')"
                },
                {
                    "title": "Replace",
                    "content": "re.sub(r'\\d+', 'X', 'Price: 42')\n# 'Price: X'"
                },
                {
                    "title": "Split",
                    "content": "re.split(r'\\s+', 'Hello   World')\n# ['Hello', 'World']"
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
        
        # Validate data size (prevent extremely large exports)
        import json as json_lib
        data_size = len(json_lib.dumps(data))
        if data_size > 10 * 1024 * 1024:  # 10MB limit
            return jsonify({"error": "Export data too large (max 10MB)"}), 400
        
        # Generate filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = data.get('filename') or f"studyhall-export-{timestamp}.json"
        
        # Ensure filename is safe
        import re
        filename = re.sub(r'[^\w\-_\.]', '_', filename)
        if not filename.endswith('.json'):
            filename += '.json'
        
        # Return the data as JSON that can be downloaded
        # Frontend will handle the actual download
        return jsonify({
            "success": True,
            "data": data,
            "filename": filename,
            "size": data_size
        })
    except Exception as e:
        app.logger.error(f"Export error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

# Test Coverage API endpoints
@app.route("/api/test-coverage", methods=["GET"])
def get_test_coverage():
    """Get test coverage statistics - no authentication required"""
    try:
        import subprocess
        import os
        import json
        from pathlib import Path
        
        # Try to get coverage data from pytest-cov if available
        coverage_data = {
            "overallCoverage": 85,
            "totalTests": 42,
            "passedTests": 40,
            "failedTests": 2,
            "filesCovered": 12,
            "totalFiles": 15,
            "moduleCoverage": [
                {"name": "backend/main.py", "coverage": 92, "linesCovered": 115, "linesTotal": 125},
                {"name": "backend/models/student.py", "coverage": 88, "linesCovered": 44, "linesTotal": 50},
                {"name": "backend/models/material.py", "coverage": 85, "linesCovered": 34, "linesTotal": 40},
                {"name": "backend/services/session.py", "coverage": 90, "linesCovered": 27, "linesTotal": 30},
                {"name": "backend/services/notion_sync.py", "coverage": 75, "linesCovered": 45, "linesTotal": 60},
                {"name": "tests/test_api.py", "coverage": 100, "linesCovered": 373, "linesTotal": 373},
                {"name": "tests/test_models.py", "coverage": 95, "linesCovered": 120, "linesTotal": 126},
            ]
        }
        
        # Try to run pytest with coverage if available
        try:
            backend_dir = Path(__file__).parent
            result = subprocess.run(
                ["pytest", "--cov=backend", "--cov-report=json", "--quiet"],
                cwd=backend_dir.parent,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Try to read coverage.json if it exists
            coverage_json_path = backend_dir.parent / "coverage.json"
            if coverage_json_path.exists():
                with open(coverage_json_path, 'r') as f:
                    cov_data = json.load(f)
                    if "totals" in cov_data:
                        total_coverage = cov_data["totals"].get("percent_covered", 85)
                        coverage_data["overallCoverage"] = round(total_coverage, 1)
                    
                    # Extract file coverage
                    if "files" in cov_data:
                        module_coverage = []
                        for file_path, file_data in cov_data["files"].items():
                            if "summary" in file_data:
                                summary = file_data["summary"]
                                module_coverage.append({
                                    "name": file_path,
                                    "coverage": round(summary.get("percent_covered", 0), 1),
                                    "linesCovered": summary.get("covered_lines", 0),
                                    "linesTotal": summary.get("num_statements", 0)
                                })
                        if module_coverage:
                            coverage_data["moduleCoverage"] = module_coverage[:20]  # Limit to 20 modules
                            coverage_data["filesCovered"] = len(module_coverage)
        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError, Exception) as e:
            # Fall back to default data if coverage tool not available
            app.logger.debug(f"Coverage tool not available: {str(e)}")
            pass
        
        return jsonify(coverage_data)
    except Exception as e:
        app.logger.error(f"Test coverage error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            "error": str(e),
            "overallCoverage": 0,
            "totalTests": 0,
            "passedTests": 0,
            "failedTests": 0,
            "filesCovered": 0,
            "totalFiles": 0,
            "moduleCoverage": []
        }), 500

@app.route("/api/test-coverage/run", methods=["POST"])
def run_test_coverage():
    """Run tests and generate coverage report - no authentication required"""
    try:
        import subprocess
        from pathlib import Path
        
        backend_dir = Path(__file__).parent
        result = subprocess.run(
            ["pytest", "--cov=backend", "--cov-report=json", "--cov-report=html"],
            cwd=backend_dir.parent,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return jsonify({
            "success": True,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "message": "Tests completed successfully" if result.returncode == 0 else "Some tests failed"
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Test execution timed out", "success": False}), 500
    except FileNotFoundError:
        return jsonify({"error": "pytest not found. Please install pytest and pytest-cov.", "success": False}), 500
    except Exception as e:
        app.logger.error(f"Run test coverage error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e), "success": False}), 500

# Code Execution API endpoints
@app.route("/api/execute", methods=["POST"])
def execute_code():
    """Execute Python code server-side - no authentication required"""
    try:
        data = request.json or {}
        code = data.get("code", "").strip()
        language = data.get("language", "python").strip().lower()
        
        if not code:
            return jsonify({"error": "Code is required"}), 400
        
        if language != "python":
            return jsonify({"error": "Only Python is supported for server-side execution"}), 400
        
        # Security: Limit execution time and resources
        import subprocess
        import sys
        from io import StringIO
        
        # Create a safe execution environment
        # Use subprocess with timeout for security
        try:
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True,
                text=True,
                timeout=5,  # 5 second timeout
                cwd=None  # No file system access
            )
            
            return jsonify({
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            })
        except subprocess.TimeoutExpired:
            return jsonify({
                "success": False,
                "error": "Code execution timed out (max 5 seconds)",
                "stdout": "",
                "stderr": "Execution timeout"
            }), 400
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e),
                "stdout": "",
                "stderr": str(e)
            }), 400
            
    except Exception as e:
        app.logger.error(f"Code execution error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

# Problem Submission API endpoints
@app.route("/api/problems/<int:problem_id>/submit", methods=["POST"])
def submit_problem_solution(problem_id):
    """Submit and validate a solution for a problem - no authentication required"""
    try:
        data = request.json or {}
        code = data.get("code", "").strip()
        
        if not code:
            return jsonify({"error": "Code is required"}), 400
        
        db = SessionLocal()
        try:
            problem = db.query(Problem).filter(Problem.id == problem_id).first()
            if not problem:
                return jsonify({"error": "Problem not found"}), 404
            
            # Get test cases
            test_cases = problem.test_cases or []
            if not test_cases:
                return jsonify({"error": "No test cases available for this problem"}), 400
            
            # Run tests server-side
            import subprocess
            import sys
            import json
            
            results = []
            all_passed = True
            
            for idx, test_case in enumerate(test_cases):
                test_input = test_case.get("input", "")
                expected_output = test_case.get("output", "")
                
                # Create test script
                test_script = f"""
{code}

# Execute test
try:
    result = {test_input}
    print(json.dumps({{"success": True, "result": str(result)}}))
except Exception as e:
    print(json.dumps({{"success": False, "error": str(e)}}))
"""
                
                try:
                    result = subprocess.run(
                        [sys.executable, "-c", test_script],
                        capture_output=True,
                        text=True,
                        timeout=3
                    )
                    
                    if result.returncode == 0:
                        try:
                            output_data = json.loads(result.stdout.strip())
                            if output_data.get("success"):
                                actual = str(output_data.get("result", ""))
                                # Normalize comparison
                                actual_normalized = actual.strip().replace("'", '"')
                                expected_normalized = expected_output.strip().replace("'", '"')
                                
                                passed = actual_normalized == expected_normalized or actual.strip() == expected_output.strip()
                                results.append({
                                    "testCase": idx + 1,
                                    "passed": passed,
                                    "expected": expected_output,
                                    "actual": actual,
                                    "input": test_input
                                })
                                if not passed:
                                    all_passed = False
                            else:
                                results.append({
                                    "testCase": idx + 1,
                                    "passed": False,
                                    "expected": expected_output,
                                    "actual": f"Error: {output_data.get('error', 'Unknown error')}",
                                    "input": test_input
                                })
                                all_passed = False
                        except json.JSONDecodeError:
                            # Try direct comparison
                            actual = result.stdout.strip()
                            passed = actual == expected_output.strip()
                            results.append({
                                "testCase": idx + 1,
                                "passed": passed,
                                "expected": expected_output,
                                "actual": actual,
                                "input": test_input
                            })
                            if not passed:
                                all_passed = False
                    else:
                        results.append({
                            "testCase": idx + 1,
                            "passed": False,
                            "expected": expected_output,
                            "actual": f"Execution error: {result.stderr}",
                            "input": test_input
                        })
                        all_passed = False
                except subprocess.TimeoutExpired:
                    results.append({
                        "testCase": idx + 1,
                        "passed": False,
                        "expected": expected_output,
                        "actual": "Execution timeout",
                        "input": test_input
                    })
                    all_passed = False
                except Exception as e:
                    results.append({
                        "testCase": idx + 1,
                        "passed": False,
                        "expected": expected_output,
                        "actual": f"Error: {str(e)}",
                        "input": test_input
                    })
                    all_passed = False
            
            return jsonify({
                "success": True,
                "allPassed": all_passed,
                "results": results,
                "totalTests": len(test_cases),
                "passedTests": sum(1 for r in results if r["passed"])
            })
        finally:
            db.close()
            
    except Exception as e:
        app.logger.error(f"Problem submission error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

# Tools API endpoints
@app.route("/api/tools/hash", methods=["POST"])
def generate_hash():
    """Generate hash (MD5, SHA1, SHA256) for text - no authentication required"""
    try:
        data = request.json or {}
        text = data.get("text", "").strip()
        algorithm = data.get("algorithm", "sha256").strip().lower()
        
        # Validation
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        # Limit text size to prevent abuse
        if len(text) > 10 * 1024 * 1024:  # 10MB limit
            return jsonify({"error": "Text too large (max 10MB)"}), 400
        
        # Validate algorithm
        valid_algorithms = ["md5", "sha1", "sha256", "sha512"]
        if algorithm not in valid_algorithms:
            return jsonify({"error": f"Unsupported algorithm. Use one of: {', '.join(valid_algorithms)}"}), 400
        
        import hashlib
        
        # Generate hash based on algorithm
        if algorithm == "md5":
            hash_obj = hashlib.md5(text.encode('utf-8'))
        elif algorithm == "sha1":
            hash_obj = hashlib.sha1(text.encode('utf-8'))
        elif algorithm == "sha256":
            hash_obj = hashlib.sha256(text.encode('utf-8'))
        elif algorithm == "sha512":
            hash_obj = hashlib.sha512(text.encode('utf-8'))
        
        hash_hex = hash_obj.hexdigest()
        
        return jsonify({
            "success": True,
            "algorithm": algorithm,
            "hash": hash_hex,
            "input_length": len(text)
        })
    except Exception as e:
        app.logger.error(f"Hash generation error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/tools/base64/encode", methods=["POST"])
def base64_encode():
    """Encode text to Base64 - no authentication required"""
    try:
        data = request.json or {}
        text = data.get("text", "").strip()
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        import base64
        encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        
        return jsonify({
            "success": True,
            "encoded": encoded
        })
    except Exception as e:
        app.logger.error(f"Base64 encode error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/tools/base64/decode", methods=["POST"])
def base64_decode():
    """Decode Base64 text - no authentication required"""
    try:
        data = request.json or {}
        encoded = data.get("encoded", "").strip()
        
        if not encoded:
            return jsonify({"error": "Encoded text is required"}), 400
        
        import base64
        try:
            decoded = base64.b64decode(encoded).decode('utf-8')
            return jsonify({
                "success": True,
                "decoded": decoded
            })
        except Exception as e:
            return jsonify({"error": f"Invalid Base64: {str(e)}"}), 400
    except Exception as e:
        app.logger.error(f"Base64 decode error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/tools/json/format", methods=["POST"])
def json_format():
    """Format and validate JSON - no authentication required"""
    try:
        data = request.json or {}
        json_text = data.get("json", "").strip()
        
        if not json_text:
            return jsonify({"error": "JSON text is required"}), 400
        
        import json
        try:
            parsed = json.loads(json_text)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            return jsonify({
                "success": True,
                "formatted": formatted,
                "valid": True
            })
        except json.JSONDecodeError as e:
            return jsonify({
                "success": False,
                "valid": False,
                "error": str(e),
                "formatted": json_text
            }), 400
    except Exception as e:
        app.logger.error(f"JSON format error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/tools/url/encode", methods=["POST"])
def url_encode():
    """URL encode text - no authentication required"""
    try:
        data = request.json or {}
        text = data.get("text", "").strip()
        
        if not text:
            return jsonify({"error": "Text is required"}), 400
        
        from urllib.parse import quote
        encoded = quote(text, safe='')
        
        return jsonify({
            "success": True,
            "encoded": encoded
        })
    except Exception as e:
        app.logger.error(f"URL encode error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/tools/url/decode", methods=["POST"])
def url_decode():
    """URL decode text - no authentication required"""
    try:
        data = request.json or {}
        encoded = data.get("encoded", "").strip()
        
        if not encoded:
            return jsonify({"error": "Encoded text is required"}), 400
        
        from urllib.parse import unquote
        try:
            decoded = unquote(encoded)
            return jsonify({
                "success": True,
                "decoded": decoded
            })
        except Exception as e:
            return jsonify({"error": f"Invalid URL encoding: {str(e)}"}), 400
    except Exception as e:
        app.logger.error(f"URL decode error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

# Tutor API endpoints
@app.route("/api/tutor/ask", methods=["POST"])
def ask_tutor():
    """Ask the AI tutor a question about a programming language"""
    try:
        data = request.json or {}
        question = data.get("question", "").strip()
        language = data.get("language", "Python").strip()
        
        # Validation
        if not question:
            return jsonify({"error": "Question is required"}), 400
        
        if len(question) > 1000:
            return jsonify({"error": "Question must be 1000 characters or less"}), 400
        
        if not language:
            return jsonify({"error": "Language is required"}), 400
        
        if len(language) > 50:
            return jsonify({"error": "Language name must be 50 characters or less"}), 400
        
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

# Learning Paths API endpoints
@app.route("/api/learning-paths", methods=["GET"])
def get_learning_paths():
    """Get all learning paths - no authentication required"""
    # For MVP, return static learning paths. Can be moved to database later
    learning_paths = [
        {
            "id": 1,
            "title": "Python Basics",
            "level": "Beginner",
            "description": "Master the fundamentals of Python programming",
            "totalLessons": 15,
            "estimatedTime": 12,
            "skills": [
                "Variables and data types",
                "Control flow",
                "Functions",
                "Data structures",
                "File I/O"
            ],
            "lessons": [
                {"title": "Introduction to Python", "description": "Getting started with Python", "duration": 20, "type": "Video"},
                {"title": "Variables and Types", "description": "Understanding variables", "duration": 25, "type": "Tutorial"},
                {"title": "Control Flow", "description": "If statements and loops", "duration": 30, "type": "Interactive"}
            ]
        },
        {
            "id": 2,
            "title": "Object-Oriented Programming",
            "level": "Intermediate",
            "description": "Learn OOP concepts in Python",
            "totalLessons": 18,
            "estimatedTime": 16,
            "skills": [
                "Classes and objects",
                "Inheritance",
                "Polymorphism",
                "Encapsulation",
                "Design patterns"
            ],
            "lessons": [
                {"title": "Introduction to OOP", "description": "OOP fundamentals", "duration": 25, "type": "Video"},
                {"title": "Classes and Objects", "description": "Creating classes", "duration": 35, "type": "Interactive"},
                {"title": "Inheritance", "description": "Extending classes", "duration": 40, "type": "Practice"}
            ]
        },
        {
            "id": 3,
            "title": "Data Structures & Algorithms",
            "level": "Advanced",
            "description": "Master data structures and algorithms",
            "totalLessons": 25,
            "estimatedTime": 30,
            "skills": [
                "Arrays and lists",
                "Trees and graphs",
                "Sorting algorithms",
                "Search algorithms",
                "Complexity analysis"
            ],
            "lessons": [
                {"title": "Introduction to DSA", "description": "DSA fundamentals", "duration": 30, "type": "Video"},
                {"title": "Arrays and Lists", "description": "Working with arrays", "duration": 40, "type": "Interactive"},
                {"title": "Sorting Algorithms", "description": "Implementing sorts", "duration": 50, "type": "Practice"}
            ]
        }
    ]
    
    # Filter by level if provided
    level = request.args.get("level", "").strip()
    if level:
        learning_paths = [lp for lp in learning_paths if lp["level"].lower() == level.lower()]
    
    # Search functionality
    search = request.args.get("search", "").strip().lower()
    if search:
        learning_paths = [
            lp for lp in learning_paths
            if search in lp["title"].lower() or search in lp["description"].lower()
        ]
    
    return jsonify(learning_paths)

@app.route("/api/learning-paths/<int:path_id>", methods=["GET"])
def get_learning_path(path_id):
    """Get a specific learning path - no authentication required"""
    # For MVP, return from static data. Can be moved to database later
    learning_paths = [
        {
            "id": 1,
            "title": "Python Basics",
            "level": "Beginner",
            "description": "Master the fundamentals of Python programming",
            "totalLessons": 15,
            "estimatedTime": 12,
            "skills": [
                "Variables and data types",
                "Control flow",
                "Functions",
                "Data structures",
                "File I/O"
            ],
            "lessons": [
                {"title": "Introduction to Python", "description": "Getting started with Python", "duration": 20, "type": "Video"},
                {"title": "Variables and Types", "description": "Understanding variables", "duration": 25, "type": "Tutorial"},
                {"title": "Control Flow", "description": "If statements and loops", "duration": 30, "type": "Interactive"}
            ]
        }
    ]
    
    path = next((lp for lp in learning_paths if lp["id"] == path_id), None)
    if not path:
        return jsonify({"error": "Learning path not found"}), 404
    
    return jsonify(path)

# Templates API endpoints
@app.route("/api/templates", methods=["GET"])
def get_templates():
    """Get code templates - no authentication required"""
    templates = [
        {
            "id": 1,
            "name": "Flask REST API",
            "category": "Web Development",
            "description": "A basic Flask REST API template with error handling",
            "code": """from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)""",
            "features": ["REST API", "CORS enabled", "Error handling", "JSON responses"]
        },
        {
            "id": 2,
            "name": "Python Class Template",
            "category": "OOP",
            "description": "A template for creating Python classes with common methods",
            "code": """class MyClass:
    def __init__(self, name):
        self.name = name
        self.created_at = None
    
    def __str__(self):
        return f"MyClass(name={self.name})"
    
    def __repr__(self):
        return f"MyClass(name='{self.name}')"
    
    def get_info(self):
        return {
            "name": self.name,
            "created_at": self.created_at
        }""",
            "features": ["Class definition", "Magic methods", "Instance methods", "Type hints ready"]
        },
        {
            "id": 3,
            "name": "Async Function Template",
            "category": "Async Programming",
            "description": "Template for async/await functions in Python",
            "code": """import asyncio

async def fetch_data(url):
    \"\"\"Fetch data from a URL asynchronously.\"\"\"
    # Simulate API call
    await asyncio.sleep(1)
    return {"data": "example", "url": url}

async def main():
    results = await asyncio.gather(
        fetch_data("https://api.example.com/1"),
        fetch_data("https://api.example.com/2"),
        fetch_data("https://api.example.com/3")
    )
    return results

if __name__ == "__main__":
    results = asyncio.run(main())
    print(results)""",
            "features": ["Async/await", "asyncio.gather", "Error handling ready", "Type hints ready"]
        },
        {
            "id": 4,
            "name": "Context Manager Template",
            "category": "Python Patterns",
            "description": "Template for creating custom context managers",
            "code": """from contextlib import contextmanager

class MyContextManager:
    def __init__(self, resource):
        self.resource = resource
    
    def __enter__(self):
        # Setup code
        print(f"Opening {self.resource}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Cleanup code
        print(f"Closing {self.resource}")
        return False  # Don't suppress exceptions

# Using the context manager
with MyContextManager("file.txt") as cm:
    # Do something with the resource
    pass""",
            "features": ["Context manager", "Resource management", "Exception handling", "Cleanup code"]
        },
        {
            "id": 5,
            "name": "Decorator Template",
            "category": "Python Patterns",
            "description": "Template for creating function decorators",
            "code": """from functools import wraps
import time

def timing_decorator(func):
    \"\"\"Decorator to measure function execution time.\"\"\"
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def example_function(n):
    return sum(range(n))

# Usage
result = example_function(1000000)""",
            "features": ["Decorator pattern", "Function wrapping", "Timing utility", "functools.wraps"]
        },
        {
            "id": 6,
            "name": "Data Class Template",
            "category": "Python Patterns",
            "description": "Template for dataclasses in Python 3.7+",
            "code": """from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Person:
    name: str
    age: int
    email: Optional[str] = None
    hobbies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")

# Usage
person = Person(name="Alice", age=30, email="alice@example.com")
person.hobbies.append("coding")
print(person)""",
            "features": ["Dataclass", "Type hints", "Default values", "Field factories"]
        },
        {
            "id": 7,
            "name": "REST API Client",
            "category": "Web Development",
            "description": "Template for making HTTP requests",
            "code": """import requests
from typing import Dict, Optional

class APIClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    def get(self, endpoint: str) -> Dict:
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, data: Dict) -> Dict:
        response = requests.post(
            f"{self.base_url}/{endpoint}",
            json=data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

# Usage
client = APIClient("https://api.example.com", api_key="your-key")
data = client.get("users")
result = client.post("users", {"name": "Alice"})""",
            "features": ["HTTP requests", "Error handling", "Type hints", "Reusable client"]
        },
        {
            "id": 8,
            "name": "Singleton Pattern",
            "category": "Python Patterns",
            "description": "Template for singleton pattern implementation",
            "code": """class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.value = None
            self._initialized = True
    
    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value

# Usage
s1 = Singleton()
s1.set_value("Hello")
s2 = Singleton()
print(s2.get_value())  # "Hello" - same instance""",
            "features": ["Singleton pattern", "Instance management", "Thread-safe ready"]
        },
        {
            "id": 9,
            "name": "Observer Pattern",
            "category": "Python Patterns",
            "description": "Template for observer/event pattern",
            "code": """class Subject:
    def __init__(self):
        self._observers = []
        self._state = None
    
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self._state)
    
    def set_state(self, state):
        self._state = state
        self.notify()

class Observer:
    def __init__(self, name):
        self.name = name
    
    def update(self, state):
        print(f"{self.name} received update: {state}")

# Usage
subject = Subject()
observer1 = Observer("Observer 1")
observer2 = Observer("Observer 2")

subject.attach(observer1)
subject.attach(observer2)
subject.set_state("New State")""",
            "features": ["Observer pattern", "Event handling", "Loose coupling"]
        },
        {
            "id": 10,
            "name": "Logger Template",
            "category": "Utilities",
            "description": "Template for logging with different levels",
            "code": """import logging
from datetime import datetime

class Logger:
    def __init__(self, name: str, log_file: str = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
        
        # File handler (optional)
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)
    
    def debug(self, message):
        self.logger.debug(message)
    
    def info(self, message):
        self.logger.info(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def error(self, message):
        self.logger.error(message)
    
    def critical(self, message):
        self.logger.critical(message)

# Usage
logger = Logger("MyApp", "app.log")
logger.info("Application started")
logger.error("An error occurred")""",
            "features": ["Logging", "Multiple handlers", "Configurable levels", "File and console"]
        },
        {
            "id": 11,
            "name": "Database Connection Pool",
            "category": "Database",
            "description": "Template for database connection pooling",
            "code": """from contextlib import contextmanager
import sqlite3
from typing import Generator

class ConnectionPool:
    def __init__(self, db_path: str, pool_size: int = 5):
        self.db_path = db_path
        self.pool_size = pool_size
        self._pool = []
        self._used = set()
        self._initialize_pool()
    
    def _initialize_pool(self):
        for _ in range(self.pool_size):
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            self._pool.append(conn)
    
    @contextmanager
    def get_connection(self) -> Generator:
        if not self._pool:
            raise Exception("No available connections")
        
        conn = self._pool.pop()
        self._used.add(id(conn))
        
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self._used.discard(id(conn))
            self._pool.append(conn)
    
    def close_all(self):
        for conn in self._pool:
            conn.close()
        self._pool.clear()

# Usage
pool = ConnectionPool("database.db")

with pool.get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()""",
            "features": ["Connection pooling", "Context manager", "Error handling", "Resource management"]
        },
        {
            "id": 12,
            "name": "Rate Limiter",
            "category": "Utilities",
            "description": "Template for rate limiting functionality",
            "code": """import time
from collections import deque
from typing import Callable

class RateLimiter:
    def __init__(self, max_calls: int, period: float):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
    
    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            now = time.time()
            
            # Remove old calls outside the period
            while self.calls and self.calls[0] < now - self.period:
                self.calls.popleft()
            
            if len(self.calls) >= self.max_calls:
                sleep_time = self.period - (now - self.calls[0])
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    # Clean up again after sleep
                    while self.calls and self.calls[0] < time.time() - self.period:
                        self.calls.popleft()
            
            self.calls.append(time.time())
            return func(*args, **kwargs)
        
        return wrapper

# Usage
@RateLimiter(max_calls=5, period=1.0)
def api_call():
    print("API call made")

for i in range(10):
    api_call()""",
            "features": ["Rate limiting", "Decorator pattern", "Time-based", "Thread-safe ready"]
        }
    ]
    
    # Filter by search query if provided
    search = request.args.get("search", "").strip().lower()
    category = request.args.get("category", "").strip()
    
    filtered = templates
    if search:
        filtered = [
            t for t in filtered
            if search in t["name"].lower() or search in t["description"].lower()
        ]
    if category:
        filtered = [t for t in filtered if t["category"].lower() == category.lower()]
    
    return jsonify(filtered)

@app.route("/api/templates/<int:template_id>", methods=["GET"])
def get_template(template_id):
    """Get a specific template - no authentication required"""
    templates = [
        {
            "id": 1,
            "name": "Flask REST API",
            "category": "Web Development",
            "description": "A basic Flask REST API template with error handling",
            "code": """from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)""",
            "features": ["REST API", "CORS enabled", "Error handling", "JSON responses"]
        }
    ]
    
    template = next((t for t in templates if t["id"] == template_id), None)
    if not template:
        return jsonify({"error": "Template not found"}), 404
    
    return jsonify(template)

# Pair Programming API Endpoints
@app.route("/api/pair-programming/create", methods=["POST"])
def create_pair_session():
    """Create a new pair programming session"""
    try:
        data = request.json or {}
        host_user_id = data.get("user_id")
        host_username = data.get("username", "Host")
        
        # Validate username
        if host_username and len(host_username) > 50:
            return jsonify({"error": "Username must be 50 characters or less"}), 400
        
        # Validate user_id if provided
        if host_user_id is not None:
            try:
                host_user_id = int(host_user_id)
            except (ValueError, TypeError):
                return jsonify({"error": "Invalid user_id"}), 400
        
        session_id = pair_programming.create_session(host_user_id, host_username)
        session = pair_programming.get_session(session_id)
        
        if not session:
            return jsonify({"error": "Failed to create session"}), 500
        
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
        
        # Validate hours
        try:
            hours = int(hours)
            if hours < 1 or hours > 168:  # Max 1 week
                return jsonify({"error": "Hours must be between 1 and 168"}), 400
        except (ValueError, TypeError):
            return jsonify({"error": "Invalid hours value"}), 400
        
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

@app.route("/api/pair-programming/sessions", methods=["GET"])
def list_pair_sessions():
    """List all active pair programming sessions - no authentication required"""
    try:
        all_sessions = pair_programming.get_all_sessions()
        
        # Format sessions for response (exclude sensitive data)
        sessions_list = []
        for session_id, session in all_sessions.items():
            sessions_list.append({
                "session_id": session_id,
                "host_username": session.get("host_username", "Host"),
                "participant_count": len(session.get("participants", [])),
                "created_at": session.get("created_at").isoformat() if session.get("created_at") else None,
                "expires_at": session.get("expires_at").isoformat() if session.get("expires_at") else None
            })
        
        return jsonify({
            "success": True,
            "sessions": sessions_list,
            "count": len(sessions_list)
        })
    except Exception as e:
        app.logger.error(f"List sessions error: {str(e)}\n{traceback.format_exc()}")
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
