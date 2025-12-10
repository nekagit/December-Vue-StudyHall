# Development Guide

Complete guide for setting up and developing the StudyHall Platform.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 18+**: [Download Node.js](https://nodejs.org/)
- **npm**: Comes with Node.js
- **Git**: [Download Git](https://git-scm.com/downloads)

## Initial Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd December-Vue-StudyHall
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Return to project root
cd ..
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Return to project root
cd ..
```

### 4. Initialize Database

```bash
# Activate backend virtual environment first
source backend/.venv/bin/activate  # On Windows: backend\.venv\Scripts\activate

# Initialize database
python backend/init_db.py
```

This creates the SQLite database and a default student account:
- **Email**: `student@studyhall.com`
- **Password**: `password123`

## Development Workflow

### Running Development Servers

The easiest way to run both frontend and backend in development mode:

```bash
./manage.py dev
```

This will:
- Start the Flask backend on `http://localhost:5000`
- Start the Vite dev server on `http://localhost:5173`
- Proxy `/api/*` requests from frontend to backend

### Running Servers Separately

If you prefer to run servers separately:

**Backend**:
```bash
source backend/.venv/bin/activate
python backend/main.py
```

**Frontend**:
```bash
cd frontend
npm run dev
```

### Building for Production

```bash
# Build frontend
./manage.py build

# Serve production build (runs backend + serves static frontend)
./manage.py serve
```

## Project Structure

```
December-Vue-StudyHall/
├── backend/
│   ├── main.py              # Flask API application
│   ├── database.py          # SQLAlchemy database setup
│   ├── init_db.py           # Database initialization script
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── student.py       # Student model
│   │   ├── material.py      # Material model
│   │   ├── progress.py      # MaterialProgress model
│   │   └── bookmark.py      # Bookmark model
│   ├── services/            # Business logic services
│   │   ├── auth.py          # Authentication service
│   │   ├── session.py       # Session management
│   │   ├── notion_sync.py   # Notion integration
│   │   └── test_runner.py   # Test execution service
│   ├── tests/               # Backend tests
│   │   ├── conftest.py      # Pytest configuration
│   │   ├── test_models.py
│   │   ├── test_auth_service.py
│   │   ├── test_session_service.py
│   │   └── test_api.py
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.vue          # Root Vue component
│   │   ├── main.ts          # Entry point with router
│   │   ├── style.scss       # TailwindCSS imports
│   │   ├── views/           # Page components
│   │   │   ├── Home.vue
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── Dashboard.vue
│   │   │   ├── Materials.vue
│   │   │   ├── MaterialDetail.vue
│   │   │   ├── Bookmarks.vue
│   │   │   ├── Compiler.vue
│   │   │   ├── Profile.vue
│   │   │   └── TestDashboard.vue
│   │   ├── components/      # Reusable components
│   │   │   ├── HelloWorld.vue
│   │   │   └── PythonRunner.vue
│   │   └── utils/           # Utility functions
│   │       └── mount.ts
│   ├── tests/               # Frontend tests
│   ├── vite.config.ts       # Vite configuration
│   ├── tailwind.config.js   # TailwindCSS configuration
│   ├── package.json         # Node dependencies
│   └── index.html           # HTML entry point
│
├── manage.py                # Management script
├── README.md                # Project overview
├── API.md                   # API documentation
├── DEVELOPMENT.md           # This file
├── DEPLOYMENT.md            # Deployment guide
├── CONTRIBUTING.md          # Contribution guidelines
└── TESTING.md               # Testing guide
```

## Code Style

### Python (Backend)

- Follow **PEP 8** style guide
- Use **type hints** for all function parameters and return types
- Maximum line length: 88 characters (Black formatter default)
- Use 4 spaces for indentation
- Use docstrings for functions and classes

**Example**:
```python
def authenticate_student(db: Session, email: str, password: str) -> Optional[Student]:
    """Authenticate a student with email and password.
    
    Args:
        db: Database session
        email: Student email address
        password: Plain text password
        
    Returns:
        Student object if authenticated, None otherwise
    """
    student = db.query(Student).filter(Student.email == email).first()
    if student and verify_password(password, student.password_hash):
        return student
    return None
```

### TypeScript/Vue (Frontend)

- Use **Composition API** (`<script setup>`) for all Vue components
- Use **TypeScript strict mode**
- Use **TailwindCSS** for all styling (no custom CSS except imports)
- Use **Vue Router** for navigation
- Use **async/await** for API calls

**Example**:
```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const materials = ref<Material[]>([])

async function fetchMaterials(): Promise<void> {
  const response = await fetch('/api/materials')
  materials.value = await response.json()
}

onMounted(() => {
  fetchMaterials()
})
</script>
```

## Database Management

### SQLite Database Location

The SQLite database is created at: `backend/studyhall.db`

### Database Migrations

Currently, the project uses manual schema updates. For production, consider using Alembic for migrations:

```bash
# Install Alembic
pip install alembic

# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

### Resetting Database

To reset the database:

```bash
# Delete database file
rm backend/studyhall.db

# Reinitialize
python backend/init_db.py
```

## Environment Variables

Create a `.env` file in the project root (or set environment variables):

```bash
# Flask
SECRET_KEY=your-secret-key-here

# Notion Integration (optional)
NOTION_API_KEY=your-notion-api-key
NOTION_DATABASE_ID=your-database-id
```

## Debugging

### Backend Debugging

Flask runs in debug mode by default in development. To enable more verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Frontend Debugging

- Use browser DevTools (F12)
- Vue DevTools extension for Vue component inspection
- Network tab to inspect API requests

### Database Inspection

Use SQLite command-line tool:

```bash
sqlite3 backend/studyhall.db

# List tables
.tables

# View schema
.schema students

# Query data
SELECT * FROM students;
```

## Testing

See [TESTING.md](./TESTING.md) for complete testing guide.

**Quick test commands**:

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

## Common Tasks

### Adding a New API Endpoint

1. Add route in `backend/main.py`
2. Add business logic in `backend/services/` if needed
3. Add test in `backend/tests/test_api.py`
4. Update `API.md` documentation

### Adding a New Vue Page

1. Create component in `frontend/src/views/`
2. Add route in `frontend/src/main.ts`
3. Add navigation link in `frontend/src/App.vue` if needed
4. Add test in `frontend/tests/views/`

### Adding a New Database Model

1. Create model in `backend/models/`
2. Import in `backend/models/__init__.py`
3. Update `backend/database.py` if needed
4. Add test in `backend/tests/test_models.py`

## Troubleshooting

### Port Already in Use

If port 5000 or 5173 is already in use:

**Backend** (change port in `backend/main.py`):
```python
app.run(debug=True, port=5001)  # Change port
```

**Frontend** (change port in `frontend/vite.config.ts`):
```typescript
server: {
  port: 5174  // Change port
}
```

### Module Not Found Errors

**Backend**:
```bash
# Ensure virtual environment is activated
source backend/.venv/bin/activate

# Reinstall dependencies
pip install -r backend/requirements.txt
```

**Frontend**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Database Locked Errors

SQLite may lock if multiple processes access it. Ensure only one Flask instance is running.

### CORS Errors

Ensure CORS origins in `backend/main.py` match your frontend URL.

## IDE Setup

### VS Code

Recommended extensions:
- **Python**: Python extension by Microsoft
- **Volar**: Vue 3 language support
- **Tailwind CSS IntelliSense**: Tailwind autocomplete
- **ESLint**: JavaScript/TypeScript linting
- **Prettier**: Code formatting

### PyCharm

- Configure Python interpreter to use `backend/.venv`
- Mark `frontend/` as excluded from Python inspection
- Enable TypeScript support

## Git Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "Add feature"`
3. Push branch: `git push origin feature/your-feature`
4. Create pull request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed contribution guidelines.

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Vue 3 Documentation](https://vuejs.org/)
- [Vite Documentation](https://vitejs.dev/)
- [TailwindCSS Documentation](https://tailwindcss.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Notion API Documentation](https://developers.notion.com/)
