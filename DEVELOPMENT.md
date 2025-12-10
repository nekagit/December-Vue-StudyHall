# Development Guide

Complete guide for developing the StudyHall Platform.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Code Style](#code-style)
- [Backend Development](#backend-development)
- [Frontend Development](#frontend-development)
- [Database Development](#database-development)
- [Testing](#testing)
- [Debugging](#debugging)
- [Common Tasks](#common-tasks)

## Getting Started

### Prerequisites

Ensure you have the following installed:

- **Python 3.9+** - Check with `python3 --version`
- **Node.js 18+** - Check with `node --version`
- **npm** - Check with `npm --version`
- **Git** - Check with `git --version`

### Initial Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd December-Vue-StudyHall
   ```

2. **Set up backend:**
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up frontend:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Initialize database:**
   ```bash
   source backend/.venv/bin/activate
   python backend/init_db.py
   ```

5. **Start development servers:**
   ```bash
   ./manage.py dev
   ```

## Development Environment

### Environment Variables

Create a `.env` file in the project root (optional, for local development):

```bash
SECRET_KEY=your-dev-secret-key
NOTION_API_KEY=your-notion-api-key
NOTION_DATABASE_ID=your-database-id
```

### Development Servers

The `./manage.py dev` command starts both servers:

- **Backend**: http://localhost:5000
- **Frontend**: http://localhost:5173

The frontend dev server (Vite) automatically proxies `/api/*` requests to the backend.

### Hot Reload

Both servers support hot reload:
- **Backend**: Flask debug mode (auto-reload on file changes)
- **Frontend**: Vite HMR (Hot Module Replacement)

## Project Structure

### Backend Structure

```
backend/
├── main.py              # Flask app and routes
├── database.py          # SQLAlchemy setup
├── init_db.py           # Database initialization
├── requirements.txt     # Python dependencies
├── models/              # Database models
│   ├── __init__.py
│   ├── student.py
│   ├── material.py
│   ├── progress.py
│   └── bookmark.py
└── services/            # Business logic
    ├── auth.py          # Authentication
    ├── session.py       # Session management
    └── notion_sync.py   # Notion integration
```

### Frontend Structure

```
frontend/
├── src/
│   ├── views/           # Page components (routes)
│   │   ├── Home.vue
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   ├── Materials.vue
│   │   ├── MaterialDetail.vue
│   │   └── Compiler.vue
│   ├── components/      # Reusable components
│   │   └── PythonRunner.vue
│   ├── App.vue          # Root component
│   ├── main.ts          # Entry point + router
│   └── style.scss       # TailwindCSS imports
├── vite.config.ts       # Vite configuration
├── tailwind.config.js   # TailwindCSS config
└── package.json         # Dependencies
```

## Code Style

### Python

- Follow **PEP 8** style guide
- Use **type hints** for all function parameters and return types
- Maximum line length: 100 characters
- Use 4 spaces for indentation

**Example:**
```python
from typing import Optional
from sqlalchemy.orm import Session

def authenticate_student(
    db: Session, 
    email: str, 
    password: str
) -> Optional[Student]:
    """Authenticate a student by email and password."""
    student = db.query(Student).filter(Student.email == email).first()
    if student and verify_password(password, student.password_hash):
        return student
    return None
```

### TypeScript/Vue

- Use **Composition API** (`<script setup>`) for all components
- Use **TypeScript strict mode**
- Use **TailwindCSS** for styling (no custom CSS)
- Use **camelCase** for variables and functions
- Use **PascalCase** for components

**Example:**
```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

interface Material {
  id: number
  title: string
  content: string
}

const materials = ref<Material[]>([])
const searchQuery = ref('')

const filteredMaterials = computed(() => {
  return materials.value.filter(m => 
    m.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})
</script>

<template>
  <div class="container mx-auto p-4">
    <input 
      v-model="searchQuery" 
      class="border rounded p-2"
      placeholder="Search materials..."
    />
  </div>
</template>
```

## Backend Development

### Adding a New Endpoint

1. **Add route in `main.py`:**
   ```python
   @app.route("/api/example", methods=["GET"])
   def get_example():
       student_id = get_current_student_id()
       if not student_id:
           return jsonify({"error": "Not authenticated"}), 401
       
       # Your logic here
       return jsonify({"success": True})
   ```

2. **Add business logic in `services/` if needed:**
   ```python
   # backend/services/example.py
   def process_example(db: Session, student_id: int) -> dict:
       # Business logic
       return {"result": "data"}
   ```

### Database Models

1. **Create model in `models/`:**
   ```python
   # backend/models/example.py
   from sqlalchemy import Column, Integer, String
   from backend.database import Base
   
   class Example(Base):
       __tablename__ = "examples"
       
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String, nullable=False)
   ```

2. **Import in `models/__init__.py`:**
   ```python
   from .example import Example
   __all__ = [..., "Example"]
   ```

3. **Update database:**
   - Tables are auto-created on app start
   - For production, use Alembic migrations

### Session Management

Sessions are stored in-memory (MVP). To upgrade to Redis:

1. Install Redis and `redis` Python package
2. Update `backend/services/session.py`
3. Use Redis client instead of in-memory dict

## Frontend Development

### Adding a New Route

1. **Create view component in `src/views/`:**
   ```vue
   <!-- src/views/Example.vue -->
   <script setup lang="ts">
   // Component logic
   </script>
   
   <template>
     <div class="container mx-auto p-4">
       <!-- Your template -->
     </div>
   </template>
   ```

2. **Add route in `src/main.ts`:**
   ```typescript
   import Example from './views/Example.vue'
   
   const routes = [
     // ... existing routes
     { 
       path: '/example', 
       component: Example,
       meta: { requiresAuth: true } // If auth required
     }
   ]
   ```

### API Calls

Use `fetch` with credentials for authenticated requests:

```typescript
const response = await fetch('/api/materials', {
  credentials: 'include' // Important for cookies
})

if (!response.ok) {
  throw new Error('Failed to fetch materials')
}

const materials = await response.json()
```

### Styling with TailwindCSS

Use Tailwind utility classes:

```vue
<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold text-gray-800 mb-4">
      Title
    </h1>
    <button class="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700">
      Click me
    </button>
  </div>
</template>
```

### Components

Create reusable components in `src/components/`:

```vue
<!-- src/components/Button.vue -->
<script setup lang="ts">
interface Props {
  label: string
  variant?: 'primary' | 'secondary'
}

defineProps<Props>()
</script>

<template>
  <button 
    :class="[
      'px-4 py-2 rounded',
      variant === 'primary' ? 'bg-indigo-600 text-white' : 'bg-gray-200'
    ]"
  >
    {{ label }}
  </button>
</template>
```

## Database Development

### Database Location

- **Development**: `sql_app.db` in project root
- **Production**: Configure via `SQLALCHEMY_DATABASE_URL`

### Viewing Database

Use SQLite browser or command line:

```bash
sqlite3 sql_app.db
.tables
SELECT * FROM students;
```

### Resetting Database

```bash
rm sql_app.db
python backend/init_db.py
```

### Database Migrations

Currently, tables are auto-created. For production:

1. Install Alembic: `pip install alembic`
2. Initialize: `alembic init alembic`
3. Create migrations: `alembic revision --autogenerate -m "description"`
4. Apply: `alembic upgrade head`

## Testing

### Backend Testing

Create tests in `backend/tests/`:

```python
# backend/tests/test_auth.py
import pytest
from backend.services.auth import authenticate_student, create_student

def test_authenticate_student(db_session):
    student = create_student(db_session, "test@test.com", "Test", "password")
    authenticated = authenticate_student(db_session, "test@test.com", "password")
    assert authenticated is not None
    assert authenticated.email == "test@test.com"
```

Run tests:
```bash
pytest backend/tests/
```

### Frontend Testing

Consider adding Vitest for Vue component testing:

```bash
npm install -D vitest @vue/test-utils
```

## Debugging

### Backend Debugging

Flask debug mode is enabled in development. Use `print()` or logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/api/example")
def example():
    logging.debug("Debug message")
    return jsonify({"success": True})
```

### Frontend Debugging

Use browser DevTools:
- **Console**: `console.log()`, `console.error()`
- **Network**: Inspect API requests
- **Vue DevTools**: Install Vue DevTools browser extension

### Database Debugging

Enable SQLAlchemy logging:

```python
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

## Common Tasks

### Adding a New Feature

1. **Backend:**
   - Add model (if needed) in `models/`
   - Add service logic in `services/`
   - Add endpoint in `main.py`

2. **Frontend:**
   - Create view component in `views/`
   - Add route in `main.ts`
   - Update navigation in `App.vue` (if needed)

### Updating Dependencies

**Backend:**
```bash
pip install <package>
pip freeze > requirements.txt
```

**Frontend:**
```bash
npm install <package>
# package.json is updated automatically
```

### Building for Production

```bash
./manage.py build
```

This builds the frontend to `frontend/dist/`.

### Code Formatting

**Python:**
```bash
pip install black
black backend/
```

**TypeScript:**
```bash
npm install -D prettier
npx prettier --write frontend/src/
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

### Database Locked

Close all database connections or restart the server.

### CORS Errors

Ensure backend CORS is configured for your frontend URL in `main.py`.

### Module Not Found

- **Backend**: Ensure virtual environment is activated
- **Frontend**: Run `npm install`

## Next Steps

- Add unit tests
- Add integration tests
- Set up CI/CD
- Add code linting (flake8, ESLint)
- Add pre-commit hooks
- Set up error tracking (Sentry)
- Add logging infrastructure
