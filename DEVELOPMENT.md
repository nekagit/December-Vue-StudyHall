# Development Guide

Complete guide for setting up and developing the StudyHall Platform.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**: Check with `python3 --version`
- **Node.js 18+**: Check with `node --version`
- **npm**: Usually comes with Node.js, check with `npm --version`
- **Git**: For version control

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
```

### 3. Frontend Setup

```bash
# From project root
cd frontend

# Install dependencies
npm install

# Return to project root
cd ..
```

### 4. Database Initialization

```bash
# Make sure virtual environment is activated
source backend/.venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# Initialize database
python backend/init_db.py
```

This creates:
- SQLite database file (`backend/studyhall.db`)
- Default student account:
  - Email: `student@studyhall.com`
  - Password: `password123`

### 5. Environment Variables (Optional)

For Notion integration, create a `.env` file in the project root:

```bash
# .env
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_notion_database_id_here
SECRET_KEY=your_secret_key_for_production
```

Or export them:

```bash
export NOTION_API_KEY="your_notion_api_key_here"
export NOTION_DATABASE_ID="your_notion_database_id_here"
export SECRET_KEY="your_secret_key_for_production"
```

## Development Workflow

### Running Development Servers

The easiest way to run both frontend and backend:

```bash
./manage.py dev
```

This will:
- Start Flask backend on `http://localhost:5000`
- Start Vite dev server on `http://localhost:5173`
- Proxy `/api/*` requests from frontend to backend

### Running Servers Separately

**Backend only:**
```bash
source backend/.venv/bin/activate
python backend/main.py
```

**Frontend only:**
```bash
cd frontend
npm run dev
```

### Accessing the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **API Docs**: See `API.md`

## Project Structure

### Backend Development

#### Adding a New API Endpoint

1. Open `backend/main.py`
2. Add route handler:

```python
@app.route("/api/your-endpoint", methods=["GET"])
def your_endpoint():
    student_id = get_current_student_id()
    if not student_id:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = SessionLocal()
    try:
        # Your logic here
        return jsonify({"success": True})
    finally:
        db.close()
```

#### Adding a New Database Model

1. Create model file in `backend/models/your_model.py`:

```python
from sqlalchemy import Column, Integer, String
from backend.database import Base

class YourModel(Base):
    __tablename__ = "your_table"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
```

2. Import in `backend/models/__init__.py`:

```python
from backend.models.your_model import YourModel
```

3. Database tables are auto-created on Flask startup

#### Adding a New Service

1. Create service file in `backend/services/your_service.py`:

```python
from typing import Optional
from sqlalchemy.orm import Session

def your_service_function(db: Session, param: str) -> Optional[dict]:
    # Your business logic here
    return {"result": "success"}
```

2. Import and use in `backend/main.py`:

```python
from backend.services.your_service import your_service_function
```

### Frontend Development

#### Adding a New Route

1. Open `frontend/src/main.ts`
2. Add route to routes array:

```typescript
const routes = [
  // ... existing routes
  { 
    path: '/your-route', 
    component: YourComponent, 
    meta: { requiresAuth: true } 
  },
]
```

3. Import component:

```typescript
import YourComponent from './views/YourComponent.vue'
```

#### Creating a New View Component

1. Create file in `frontend/src/views/YourComponent.vue`:

```vue
<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold">Your Component</h1>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const data = ref(null)

onMounted(async () => {
  const response = await fetch('/api/your-endpoint')
  data.value = await response.json()
})
</script>
```

#### Creating a Reusable Component

1. Create file in `frontend/src/components/YourComponent.vue`
2. Use Composition API with `<script setup>`
3. Define props and emits:

```vue
<script setup lang="ts">
interface Props {
  title: string
  count?: number
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
})

const emit = defineEmits<{
  click: [value: string]
}>()
</script>
```

#### Making API Calls

```typescript
// GET request
const response = await fetch('/api/materials')
const materials = await response.json()

// POST request
const response = await fetch('/api/bookmarks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ material_id: 5 }),
  credentials: 'include' // Important for cookies
})
const result = await response.json()
```

## Code Style

### Python

- Follow PEP 8 style guide
- Use type hints for all functions
- Maximum line length: 100 characters
- Use 4 spaces for indentation
- Use descriptive variable and function names

Example:
```python
from typing import Optional
from sqlalchemy.orm import Session

def get_student_by_id(db: Session, student_id: int) -> Optional[Student]:
    """Get a student by their ID."""
    return db.query(Student).filter(Student.id == student_id).first()
```

### TypeScript/Vue

- Use Composition API (`<script setup>`) for all components
- Use TypeScript strict mode
- Use TailwindCSS utility classes for styling
- Prefer `const` over `let`
- Use async/await for promises

Example:
```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Material {
  id: number
  title: string
}

const materials = ref<Material[]>([])

onMounted(async () => {
  const response = await fetch('/api/materials', {
    credentials: 'include'
  })
  materials.value = await response.json()
})
</script>
```

## Database Management

### Viewing Database

You can use SQLite command-line tool:

```bash
sqlite3 backend/studyhall.db
```

Common commands:
```sql
.tables                    -- List all tables
.schema students           -- Show table schema
SELECT * FROM students;    -- Query data
```

### Resetting Database

```bash
# Delete database file
rm backend/studyhall.db

# Reinitialize
python backend/init_db.py
```

### Database Migrations

Currently, migrations are handled by SQLAlchemy auto-creation. For production:

1. Consider using Alembic for migrations
2. Create migration: `alembic revision --autogenerate -m "description"`
3. Apply migration: `alembic upgrade head`

## Testing

### Running Tests (if implemented)

```bash
# Backend tests
pytest backend/tests/

# Frontend tests
cd frontend
npm run test
```

### Manual Testing

1. **Authentication Flow**:
   - Register new account
   - Login with credentials
   - Logout
   - Access protected routes

2. **Materials**:
   - View materials list
   - Search materials
   - Filter by category
   - View material detail
   - Sync from Notion (if configured)

3. **Bookmarks**:
   - Bookmark a material
   - View bookmarks list
   - Remove bookmark

4. **Progress**:
   - Update progress on material
   - View progress statistics
   - Check dashboard stats

## Debugging

### Backend Debugging

Flask runs in debug mode by default in development:
- Automatic reload on code changes
- Detailed error pages
- Console logging

Add logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.error("Error message")
```

### Frontend Debugging

- Use browser DevTools (F12)
- Vue DevTools extension (recommended)
- Console logging:
```typescript
console.log('Debug:', data)
console.error('Error:', error)
```

### Common Issues

**Issue**: CORS errors
- **Solution**: Ensure backend CORS is configured correctly
- Check `backend/main.py` CORS settings

**Issue**: Session not persisting
- **Solution**: Ensure `credentials: 'include'` in fetch calls
- Check cookie settings in backend

**Issue**: Database locked
- **Solution**: Close any open database connections
- Restart backend server

**Issue**: Module not found
- **Solution**: Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

## Building for Production

### Build Frontend

```bash
./manage.py build
```

This creates optimized production build in `frontend/dist/`.

### Test Production Build Locally

```bash
# Build frontend
./manage.py build

# Serve production build
./manage.py serve
```

## Git Workflow

### Branching Strategy

- `master`: Production-ready code
- `develop`: Development branch
- `feature/*`: Feature branches
- `fix/*`: Bug fix branches

### Commit Messages

Use descriptive commit messages:

```
feat: Add bookmark functionality
fix: Fix session expiration issue
docs: Update API documentation
refactor: Improve database query performance
```

### Before Committing

1. Test your changes
2. Check for linting errors
3. Ensure database migrations are included (if any)
4. Update documentation if needed

## IDE Setup

### VS Code / Cursor

Recommended extensions:
- Python
- Vue Language Features (Volar)
- Tailwind CSS IntelliSense
- ESLint
- Prettier

### Settings

Create `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/bin/python",
  "python.formatting.provider": "black",
  "[python]": {
    "editor.formatOnSave": true
  },
  "[typescript]": {
    "editor.formatOnSave": true
  },
  "[vue]": {
    "editor.formatOnSave": true
  }
}
```

## Performance Optimization

### Backend

- Use database indexes for frequently queried fields
- Implement pagination for large datasets
- Cache frequently accessed data
- Use connection pooling

### Frontend

- Lazy load routes
- Code splitting for large components
- Optimize images
- Use Vue's `v-memo` for expensive lists
- Debounce search inputs

## Security Best Practices

1. **Never commit secrets**: Use `.env` files and `.gitignore`
2. **Validate all inputs**: Both frontend and backend
3. **Use HTTPS in production**: Never send credentials over HTTP
4. **Keep dependencies updated**: Regularly update packages
5. **Review authentication logic**: Ensure proper session handling

## Getting Help

- Check existing documentation files
- Review code comments
- Check API documentation (`API.md`)
- Review architecture documentation (`ARCHITECTURE.md`)

## Next Steps

After setup:
1. Explore the codebase
2. Read `API.md` for API reference
3. Read `ARCHITECTURE.md` for system design
4. Start developing features!
