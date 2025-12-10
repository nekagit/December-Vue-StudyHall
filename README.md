# StudyHall Platform

A modern learning platform for managing course materials for up to 30 students, featuring Python course content, a browser-based Python compiler, and Notion integration.

## 🚀 Features

- ✅ **Student Authentication** - Secure login/registration system (max 30 students)
- ✅ **Course Materials Management** - Browse, search, and organize learning materials
- ✅ **Progress Tracking** - Track completion status and progress percentage for each material
- ✅ **Bookmarks** - Save favorite materials for quick access
- ✅ **Notion Integration** - Sync course materials from Notion databases
- ✅ **Python Compiler** - Browser-based Python code execution using Pyodide
- ✅ **Modern UI** - Beautiful, responsive interface built with Vue.js 3 and TailwindCSS
- ✅ **Dashboard** - Overview of learning progress and recent activity

## 📋 Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [Contributing](#contributing)

## 🏗️ Architecture

This is a modern Single Page Application (SPA) with a clear separation between frontend and backend:

- **Backend**: Minimal Flask REST API (Python) - JSON endpoints only, no HTML rendering
- **Frontend**: Vue.js 3 SPA with TypeScript and TailwindCSS
- **Database**: SQLite (MVP) - easily upgradeable to PostgreSQL
- **Pattern**: Full frontend SPA with API backend

### Technology Stack

**Backend:**
- Flask - Web framework
- SQLAlchemy - ORM
- SQLite - Database (MVP)
- Flask-CORS - Cross-origin resource sharing

**Frontend:**
- Vue.js 3 - Progressive JavaScript framework
- TypeScript - Type-safe JavaScript
- TailwindCSS - Utility-first CSS framework
- Vue Router - Client-side routing
- Vite - Build tool and dev server

## 📦 Prerequisites

- **Python 3.9+** - Backend runtime
- **Node.js 18+** - Frontend runtime
- **npm** - Package manager
- **Git** - Version control

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd December-Vue-StudyHall
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

### 4. Initialize Database

```bash
source backend/.venv/bin/activate
python backend/init_db.py
```

This creates the database and a default student account:
- **Email**: `student@studyhall.com`
- **Password**: `password123`

### 5. Start Development Servers

```bash
./manage.py dev
```

This starts both servers:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

The frontend dev server automatically proxies `/api/*` requests to the backend.

## 📁 Project Structure

```
December-Vue-StudyHall/
├── backend/
│   ├── main.py              # Flask API application
│   ├── database.py          # SQLAlchemy database setup
│   ├── init_db.py           # Database initialization script
│   ├── requirements.txt     # Python dependencies
│   ├── models/              # Database models
│   │   ├── student.py       # Student model
│   │   ├── material.py      # Material model
│   │   ├── progress.py      # MaterialProgress model
│   │   └── bookmark.py      # Bookmark model
│   └── services/            # Business logic
│       ├── auth.py          # Authentication service
│       ├── session.py       # Session management
│       └── notion_sync.py   # Notion integration
│
├── frontend/
│   ├── src/
│   │   ├── views/           # Vue page components
│   │   │   ├── Home.vue
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── Materials.vue
│   │   │   ├── MaterialDetail.vue
│   │   │   └── Compiler.vue
│   │   ├── components/     # Reusable Vue components
│   │   │   └── PythonRunner.vue
│   │   ├── App.vue          # Root component
│   │   ├── main.ts          # Entry point with Vue Router
│   │   └── style.scss       # TailwindCSS imports
│   ├── vite.config.ts       # Vite configuration
│   ├── tailwind.config.js   # TailwindCSS configuration
│   ├── package.json         # Node.js dependencies
│   └── index.html           # HTML entry point
│
└── manage.py                # Management script
```

## 📚 API Documentation

See [API.md](./API.md) for complete API endpoint documentation.

### Quick API Reference

**Authentication:**
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Register
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Get current user

**Materials:**
- `GET /api/materials` - List materials (with search and category filters)
- `GET /api/materials/:id` - Get material detail
- `GET /api/materials/categories` - Get all categories
- `POST /api/materials/sync-notion` - Sync from Notion

**Progress:**
- `POST /api/progress/:id` - Update progress

**Bookmarks:**
- `GET /api/bookmarks` - Get all bookmarks
- `POST /api/bookmarks/:id` - Add bookmark
- `DELETE /api/bookmarks/:id` - Remove bookmark

**Profile:**
- `GET /api/profile` - Get profile with stats
- `PUT /api/profile` - Update profile

**Dashboard:**
- `GET /api/dashboard/stats` - Get dashboard statistics

## 🔧 Configuration

### Environment Variables

**Backend:**
- `SECRET_KEY` - Flask secret key (default: "dev-secret-key-change-in-production")
- `NOTION_API_KEY` - Notion API key for integration
- `NOTION_DATABASE_ID` - Notion database ID to sync from

**Set environment variables:**
```bash
export SECRET_KEY="your-secret-key"
export NOTION_API_KEY="your-notion-api-key"
export NOTION_DATABASE_ID="your-database-id"
```

### Notion Integration Setup

1. Create a Notion integration at https://www.notion.so/my-integrations
2. Get your API key from the integration settings
3. Share your database/page with the integration
4. Get the database ID from the Notion URL
5. Set environment variables (see above)
6. Use "Sync from Notion" button in the Materials page

## 💻 Development

See [DEVELOPMENT.md](./DEVELOPMENT.md) for detailed development guide.

### Development Commands

```bash
# Start both frontend and backend
./manage.py dev

# Build frontend for production
./manage.py build

# Run backend only
./manage.py run
```

### Code Style

- **Python**: Follow PEP 8, use type hints
- **TypeScript**: Use strict mode, Composition API for Vue components
- **Styling**: Use TailwindCSS utility classes (no custom CSS)

## 🚢 Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for deployment instructions.

### Production Build

```bash
# Build frontend
./manage.py build

# Serve production build
./manage.py serve
```

## 🗄️ Database

The application uses SQLite by default (MVP). The database file is created at `sql_app.db` in the project root.

### Database Models

- **Student** - User accounts (max 30)
- **Material** - Course materials/content
- **MaterialProgress** - Student progress tracking
- **Bookmark** - Student bookmarks

### Database Migration

Currently, the database schema is managed through SQLAlchemy models. For production, consider using Alembic for migrations.

## 🔐 Security Notes

**MVP Limitations:**
- Password hashing uses SHA-256 (upgrade to bcrypt for production)
- Session management is in-memory (upgrade to Redis for production)
- CORS is configured for localhost (configure properly for production)
- Secret key is hardcoded (use environment variable in production)

## 📖 Additional Documentation

- [API.md](./API.md) - Complete API reference
- [DEVELOPMENT.md](./DEVELOPMENT.md) - Development guide
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment guide

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT

## 🙏 Acknowledgments

- Vue.js team for the amazing framework
- Flask team for the lightweight web framework
- TailwindCSS for the utility-first CSS framework
- Pyodide for browser-based Python execution
