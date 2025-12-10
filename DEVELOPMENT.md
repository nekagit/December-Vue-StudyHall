# Development Guide

This guide covers setting up and working with the StudyHall Platform development environment.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**: Check with `python3 --version`
- **Node.js 18+**: Check with `node --version`
- **npm**: Comes with Node.js, check with `npm --version`
- **Git**: For version control

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/December-Vue-StudyHall.git
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
# Make sure virtual environment is activated
source backend/.venv/bin/activate  # On Windows: backend\.venv\Scripts\activate

# Initialize database with default student
python backend/init_db.py
```

This creates:
- SQLite database file (`studyhall.db`)
- Default student account:
  - Email: `student@studyhall.com`
  - Password: `password123`

## Development Workflow

### Starting Development Servers

The easiest way to start both frontend and backend is using the management script:

```bash
./manage.py dev
```

This will:
- Start Flask backend on `http://localhost:5000`
- Start Vite dev server on `http://localhost:5173`
- Proxy `/api/*` requests from frontend to backend

**Note**: Press `Ctrl+C` to stop both servers.

### Manual Server Startup

If you prefer to run servers separately:

**Terminal 1 - Backend:**
```bash
source backend/.venv/bin/activate
export PYTHONPATH=$(pwd)
python backend/main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Accessing the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **API Docs**: See `API.md` for endpoint documentation

## Environment Variables

### Backend Environment Variables

Create a `.env` file in the project root (optional for development):

```bash
# Secret key for Flask sessions (change in production!)
SECRET_KEY=dev-secret-key-change-in-production

# Notion integration (optional, for syncing materials)
NOTION_API_KEY=secret_...
NOTION_DATABASE_ID=...

# Database URL (optional, defaults to SQLite)
DATABASE_URL=sqlite:///studyhall.db
```

**Note**: For Notion integration, see the Notion setup section below.

### Frontend Environment Variables

Frontend uses Vite's environment variables. Create `frontend/.env`:

```bash
# API base URL (defaults to /api in dev, proxied to backend)
VITE_API_BASE_URL=/api
```

## Project Structure

```
December-Vue-StudyHall/
├── backend/              # Flask API backend
│   ├── main.py          # Flask app and routes
│   ├── database.py      # SQLAlchemy setup
│   ├── init_db.py       # Database initialization
│   ├── models/          # Database models
│   └── services/        # Business logic
├── frontend/            # Vue.js SPA
│   ├── src/
│   │   ├── views/       # Page components
│   │   ├── components/  # Reusable components
│   │   └── App.vue      # Root component
│   └── vite.config.ts   # Vite configuration
├── tests/               # Test suite
└── manage.py            # Management script
```

## Common Development Tasks

### Adding a New API Endpoint

1. **Add route** in `backend/main.py`:
```python
@app.route("/api/your-endpoint", methods=["GET"])
def your_endpoint():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    # Your logic here
    return jsonify({"success": True})
```

2. **Add business logic** in `backend/services/` if needed
3. **Test** the endpoint using curl or Postman
4. **Update** `API.md` with endpoint documentation

### Adding a New Frontend Page

1. **Create view** in `frontend/src/views/YourPage.vue`:
```vue
<template>
  <div class="container mx-auto p-4">
    <h1>Your Page</h1>
  </div>
</template>

<script setup lang="ts">
// Your component logic
</script>
```

2. **Add route** in `frontend/src/main.ts`:
```typescript
import YourPage from './views/YourPage.vue'

const routes = [
  // ... existing routes
  { path: '/your-page', component: YourPage }
]
```

3. **Add navigation link** in `frontend/src/App.vue` if needed

### Adding a New Database Model

1. **Create model** in `backend/models/your_model.py`:
```python
from sqlalchemy import Column, Integer, String
from backend.database import Base

class YourModel(Base):
    __tablename__ = "your_table"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
```

2. **Import in** `backend/models/__init__.py`:
```python
from backend.models.your_model import YourModel
```

3. **Tables are auto-created** when Flask starts (via `Base.metadata.create_all()`)

### Running Tests

```bash
# Activate virtual environment
source backend/.venv/bin/activate

# Run all tests
pytest

# Run specific test file
pytest tests/test_auth_service.py

# Run with coverage
pytest --cov=backend tests/
```

## Debugging

### Backend Debugging

Flask runs in debug mode by default in development:
- Auto-reloads on code changes
- Shows detailed error pages
- Enables Flask debugger

**Debugging Tips:**
- Use `print()` statements (remove before committing)
- Use Python debugger: `import pdb; pdb.set_trace()`
- Check Flask logs in terminal
- Use Postman/curl to test API endpoints

### Frontend Debugging

Vite provides Hot Module Replacement (HMR):
- Changes reflect immediately
- State is preserved during HMR
- Fast refresh for Vue components

**Debugging Tips:**
- Use browser DevTools (F12)
- Check Console for errors
- Use Vue DevTools browser extension
- Check Network tab for API calls
- Use `console.log()` for debugging

### Database Debugging

**View database contents:**
```bash
# SQLite command line
sqlite3 studyhall.db

# List tables
.tables

# View students
SELECT * FROM students;

# View materials
SELECT * FROM materials;

# Exit
.quit
```

**Reset database:**
```bash
# Delete database file
rm studyhall.db  # On Windows: del studyhall.db

# Reinitialize
python backend/init_db.py
```

## Notion Integration Setup

To enable Notion material syncing:

1. **Create Notion Integration**:
   - Go to https://www.notion.so/my-integrations
   - Click "New integration"
   - Name it (e.g., "StudyHall Sync")
   - Copy the API key (starts with `secret_`)

2. **Share Database with Integration**:
   - Open your Notion database/page
   - Click "..." menu → "Connections"
   - Add your integration

3. **Get Database ID**:
   - Open your Notion database in browser
   - URL format: `https://notion.so/your-workspace/DATABASE_ID?v=...`
   - Copy the `DATABASE_ID` (32-character hex string)

4. **Set Environment Variables**:
   ```bash
   export NOTION_API_KEY="secret_..."
   export NOTION_DATABASE_ID="..."
   ```

5. **Test Sync**:
   - Start dev servers
   - Login to application
   - Go to Materials page
   - Click "Sync from Notion"
   - Check for synced materials

## Building for Production

### Build Frontend

```bash
./manage.py build
```

Or manually:
```bash
cd frontend
npm run build
```

This creates `frontend/dist/` with production-ready static files.

### Serve Production Build

```bash
# Serve static files + backend
./manage.py serve
```

**Note**: For production, use a proper web server (Nginx) and WSGI server (Gunicorn). See `DEPLOYMENT.md`.

## Code Quality Tools

### Python Formatting

If you have `black` installed:
```bash
black backend/
```

### Type Checking

If you have `mypy` installed:
```bash
mypy backend/
```

### Linting

**Python** (if `flake8` is installed):
```bash
flake8 backend/
```

**TypeScript** (if ESLint is configured):
```bash
cd frontend
npm run lint
```

## Troubleshooting

### Port Already in Use

**Backend (5000):**
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
```

**Frontend (5173):**
```bash
# Find process using port 5173
lsof -i :5173  # macOS/Linux
netstat -ano | findstr :5173  # Windows
```

### Database Locked

SQLite can lock if multiple processes access it:
- Ensure only one Flask instance is running
- Close any database viewers
- Restart dev servers

### Module Not Found Errors

**Backend:**
```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=$(pwd)

# Or activate virtual environment
source backend/.venv/bin/activate
```

**Frontend:**
```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors

If you see CORS errors:
- Ensure backend CORS is configured in `backend/main.py`
- Check that frontend is using correct API URL
- Verify `vite.config.ts` proxy configuration

### TypeScript Errors

```bash
# Check TypeScript version
cd frontend
npm list typescript

# Rebuild
npm run build
```

## Useful Commands

```bash
# Start development
./manage.py dev

# Build frontend
./manage.py build

# Run backend only
./manage.py run

# Run tests
pytest

# Check Python version
python3 --version

# Check Node version
node --version

# Activate virtual environment
source backend/.venv/bin/activate

# Install new Python package
pip install package-name
pip freeze > backend/requirements.txt

# Install new npm package
cd frontend
npm install package-name
```

## IDE Setup

### VS Code

**Recommended Extensions:**
- Python
- Vue Language Features (Volar)
- Tailwind CSS IntelliSense
- ESLint
- Prettier

**Settings** (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/bin/python",
  "python.linting.enabled": true,
  "editor.formatOnSave": true
}
```

### PyCharm

- Mark `backend/` as Sources Root
- Configure Python interpreter to `.venv`
- Enable Vue.js plugin

## Getting Help

- **Documentation**: Check `README.md`, `API.md`, `ARCHITECTURE.md`
- **Issues**: Check GitHub Issues for known problems
- **Code**: Review existing code for examples
- **Community**: Reach out to maintainers

Happy coding! 🚀
