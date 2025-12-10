# StudyHall Platform

A modern learning platform for managing course materials for 30 students, featuring Python course content, a browser-based Python compiler, and Notion integration.

## Architecture

- **Backend**: Minimal Flask API (Python) - REST endpoints only
- **Frontend**: Vue.js 3 SPA + TypeScript + TailwindCSS
- **Database**: SQLite (MVP)
- **Pattern**: Full frontend SPA with API backend

## Features

- ✅ Student authentication (up to 30 students)
- ✅ Course materials management
- ✅ Notion page import/sync
- ✅ Browser-based Python compiler (Pyodide)
- ✅ Modern TailwindCSS UI
- ✅ Vue Router for navigation

## Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm

### Installation

1. **Backend Setup**:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Frontend Setup**:
```bash
cd frontend
npm install
cd ..
```

3. **Initialize Database**:
```bash
source backend/.venv/bin/activate
python backend/init_db.py
```

4. **Development Mode** (runs both frontend and backend):
```bash
./manage.py dev
```

Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

5. **Production Build**:
```bash
./manage.py build
./manage.py serve
```

## Usage

### Default Credentials

After running `init_db.py`, you can login with:
- Email: `student@studyhall.com`
- Password: `password123`

### Notion Integration

To sync materials from Notion:

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Get your API key
3. Share your database/page with the integration
4. Set environment variables:
```bash
export NOTION_API_KEY="your_api_key"
export NOTION_DATABASE_ID="your_database_id"
```
5. Click "Sync from Notion" in the Materials page

## Project Structure

```
backend/
  - main.py              # Flask API app
  - database.py          # SQLAlchemy setup
  - models/              # Database models
  - services/            # Business logic
  - init_db.py           # Database initialization

frontend/
  - src/
    - views/             # Vue pages (Home, Login, Materials, etc.)
    - components/        # Vue components (PythonRunner)
    - App.vue            # Root component
    - main.ts            # Entry point with router
    - style.scss         # TailwindCSS imports
  - vite.config.ts       # Build config

manage.py                # Management script
```

## Development

- Backend API runs on `http://localhost:5000`
- Frontend dev server runs on `http://localhost:5173`
- Use `./manage.py dev` for development (both servers)
- Frontend proxies `/api/*` to backend

## API Endpoints

- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Register
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user
- `GET /api/materials` - List materials
- `GET /api/materials/:id` - Get material detail
- `POST /api/materials/sync-notion` - Sync from Notion

For detailed API documentation, see [API.md](./API.md).

## Documentation

Comprehensive documentation is available:

- **[API.md](./API.md)** - Complete API reference with request/response examples
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System architecture, design decisions, and technical stack
- **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Development setup, workflow, and debugging guide
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Production deployment instructions and best practices
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Contribution guidelines and code style standards

## License

MIT
