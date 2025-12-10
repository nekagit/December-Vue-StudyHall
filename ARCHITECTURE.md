# Architecture Documentation

This document provides an overview of the StudyHall Platform architecture, design decisions, and technical stack.

## Overview

StudyHall is a modern Single Page Application (SPA) learning platform designed to manage course materials for up to 30 students. It features a clean separation between frontend and backend, with a RESTful API architecture.

## System Architecture

```
┌─────────────────┐
│   Vue.js SPA    │  Frontend (Port 5173)
│   TypeScript    │
│   TailwindCSS   │
└────────┬────────┘
         │ HTTP/REST
         │ (with CORS)
         ▼
┌─────────────────┐
│   Flask API     │  Backend (Port 5000)
│   Python        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   SQLite DB     │  Database (MVP)
│   SQLAlchemy    │
└─────────────────┘
```

## Technology Stack

### Frontend

- **Framework**: Vue.js 3 (Composition API)
- **Language**: TypeScript
- **Styling**: TailwindCSS 4.x
- **Routing**: Vue Router 4
- **Build Tool**: Vite 7
- **Python Execution**: Pyodide (browser-based Python compiler)

### Backend

- **Framework**: Flask (minimal REST API)
- **Language**: Python 3.9+
- **ORM**: SQLAlchemy
- **Database**: SQLite (MVP)
- **HTTP Client**: httpx (for Notion API)
- **Testing**: pytest

### Development Tools

- **Package Manager**: npm (frontend), pip (backend)
- **Management Script**: `manage.py` (Python script for dev/build/serve)
- **Version Control**: Git

## Project Structure

```
December-Vue-StudyHall/
├── backend/                 # Flask API backend
│   ├── main.py             # Flask app and routes
│   ├── database.py         # SQLAlchemy setup
│   ├── init_db.py          # Database initialization
│   ├── models/             # Database models
│   │   ├── student.py      # Student model
│   │   ├── material.py     # Material model
│   │   └── bookmark.py     # Bookmark model (future)
│   └── services/           # Business logic
│       ├── auth.py         # Authentication logic
│       ├── session.py      # Session management
│       └── notion_sync.py  # Notion integration
├── frontend/               # Vue.js SPA
│   ├── src/
│   │   ├── views/          # Page components
│   │   │   ├── Home.vue
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── Materials.vue
│   │   │   ├── MaterialDetail.vue
│   │   │   └── Compiler.vue
│   │   ├── components/     # Reusable components
│   │   │   └── PythonRunner.vue
│   │   ├── App.vue         # Root component
│   │   ├── main.ts         # Entry point + router
│   │   └── style.scss      # TailwindCSS imports
│   ├── vite.config.ts      # Vite configuration
│   └── tailwind.config.js  # TailwindCSS config
├── tests/                  # Test suite
│   ├── conftest.py         # pytest configuration
│   └── test_*.py           # Test files
├── manage.py               # Management script
└── README.md               # Project documentation
```

## Design Principles

### 1. Separation of Concerns

- **Backend**: Pure REST API, no HTML rendering
- **Frontend**: Complete SPA, handles all UI/UX
- **API**: JSON-only communication

### 2. Minimal Backend

The Flask backend is intentionally minimal:
- No templates or HTML rendering
- No frontend asset serving (handled by Vite)
- Focus on API endpoints only
- Business logic in service layer

### 3. Modern Frontend

- Vue 3 Composition API (`<script setup>`)
- TypeScript for type safety
- TailwindCSS for utility-first styling
- Client-side routing with Vue Router

### 4. MVP-First Approach

- SQLite for simplicity (easy to upgrade to PostgreSQL)
- In-memory sessions (upgrade to Redis later)
- Simple password hashing (upgrade to bcrypt)
- Hardcoded student limit (30 students)

## Data Flow

### Authentication Flow

```
1. User submits login form
   ↓
2. Frontend POST /api/auth/login
   ↓
3. Backend validates credentials
   ↓
4. Backend creates session token
   ↓
5. Backend sets HTTP-only cookie
   ↓
6. Frontend stores user info in component state
   ↓
7. Router guard checks session for protected routes
```

### Material Fetching Flow

```
1. User navigates to /materials
   ↓
2. Router guard validates session
   ↓
3. Frontend GET /api/materials
   ↓
4. Backend queries database
   ↓
5. Backend returns JSON array
   ↓
6. Frontend renders materials list
```

### Notion Sync Flow

```
1. User clicks "Sync from Notion"
   ↓
2. Frontend POST /api/materials/sync-notion
   ↓
3. Backend calls Notion API (async)
   ↓
4. Backend processes pages
   ↓
5. Backend creates Material records
   ↓
6. Backend returns sync count
   ↓
7. Frontend refreshes materials list
```

## Database Schema

### Students Table

```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR NOT NULL,
    password_hash VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Materials Table

```sql
CREATE TABLE materials (
    id INTEGER PRIMARY KEY,
    title VARCHAR NOT NULL,
    content TEXT,
    notion_page_id VARCHAR UNIQUE,
    notion_url VARCHAR,
    category VARCHAR,
    order_index INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);
```

## Authentication & Authorization

### Session Management

- **Storage**: In-memory dictionary (upgrade to Redis)
- **Token Format**: Random UUID string
- **Expiration**: 7 days (604800 seconds)
- **Transport**: HTTP-only cookies (secure, not accessible via JavaScript)

### Authorization

- **Route Guards**: Vue Router `beforeEach` hook
- **API Guards**: Session validation in Flask endpoints
- **Student Limit**: Hardcoded 30-student maximum

## API Design

### RESTful Principles

- **GET**: Retrieve resources
- **POST**: Create resources or perform actions
- **PUT/PATCH**: Update resources (future)
- **DELETE**: Remove resources (future)

### Endpoint Naming

- `/api/auth/*` - Authentication endpoints
- `/api/materials/*` - Material management endpoints
- Consistent use of plural nouns
- Resource IDs in URL path

### Response Format

All responses are JSON:
- **Success**: `{ "success": true, ... }` or direct resource data
- **Error**: `{ "error": "Error message" }`
- **Status Codes**: Standard HTTP status codes (200, 400, 401, 404, 500)

## Frontend Architecture

### Component Structure

- **Views**: Page-level components (routes)
- **Components**: Reusable UI components
- **App.vue**: Root component with navigation
- **main.ts**: Application entry point + router setup

### State Management

Currently using component-level state (`ref`, `reactive`). For future scaling, consider:
- Pinia (Vue's official state management)
- Vuex (legacy, but still supported)

### Styling Approach

- **TailwindCSS**: Utility-first CSS framework
- **No Custom CSS**: Except Tailwind imports
- **Responsive Design**: Mobile-first approach
- **Design System**: Indigo color scheme

## Backend Architecture

### Service Layer Pattern

Business logic is separated into service modules:
- `auth.py`: Authentication and user management
- `session.py`: Session token management
- `notion_sync.py`: Notion API integration

### Database Layer

- **ORM**: SQLAlchemy for type-safe database operations
- **Models**: Defined in `backend/models/`
- **Migrations**: Manual schema updates (consider Alembic for production)

### Error Handling

- **Validation**: Service layer validates input
- **Exceptions**: Caught and returned as JSON errors
- **Database**: Transactions with rollback on errors

## External Integrations

### Notion API

- **Purpose**: Sync course materials from Notion
- **Authentication**: API key via environment variable
- **Database**: Requires shared Notion database
- **Async**: Uses `asyncio` for async API calls

### Pyodide

- **Purpose**: Browser-based Python execution
- **Location**: Frontend component (`PythonRunner.vue`)
- **Isolation**: Runs in Web Worker for security

## Development Workflow

### Local Development

1. **Backend**: Flask dev server (auto-reload)
2. **Frontend**: Vite dev server (HMR)
3. **Proxy**: Vite proxies `/api/*` to backend
4. **Database**: SQLite file in project root

### Build Process

1. **Frontend**: `npm run build` → `dist/` folder
2. **Backend**: No build step (Python interpreted)
3. **Production**: Serve static files + Flask API

## Scalability Considerations

### Current Limitations (MVP)

- **Database**: SQLite (single file, no concurrent writes)
- **Sessions**: In-memory (lost on restart)
- **Password Security**: SHA-256 (not secure)
- **Student Limit**: Hardcoded 30

### Production Upgrades

1. **Database**: PostgreSQL with connection pooling
2. **Sessions**: Redis or database-backed sessions
3. **Password**: bcrypt with salt rounds
4. **Caching**: Redis for frequently accessed data
5. **CDN**: Serve static assets via CDN
6. **Load Balancer**: Multiple backend instances
7. **Monitoring**: Application performance monitoring
8. **Logging**: Structured logging (e.g., ELK stack)

## Security Considerations

### Current Security Measures

- HTTP-only cookies (XSS protection)
- CORS configuration
- Session-based authentication
- Password hashing (basic)

### Security Improvements Needed

1. **HTTPS**: Always use HTTPS in production
2. **Password Hashing**: Upgrade to bcrypt
3. **CSRF Protection**: Add CSRF tokens
4. **Rate Limiting**: Prevent brute force attacks
5. **Input Validation**: Sanitize all inputs
6. **SQL Injection**: Use parameterized queries (already using SQLAlchemy)
7. **XSS Protection**: Vue automatically escapes content
8. **Secret Management**: Use environment variables, not hardcoded secrets

## Testing Strategy

### Backend Tests

- **Framework**: pytest
- **Location**: `tests/` directory
- **Coverage**: Unit tests for services, integration tests for API

### Frontend Tests

- **Framework**: Not yet implemented (consider Vitest)
- **Types**: Unit tests for components, E2E tests for flows

## Deployment Architecture

### Development

- Local development servers
- SQLite database file
- Environment variables in shell

### Production (Recommended)

```
┌─────────────┐
│   Nginx     │  Reverse proxy + static files
└──────┬──────┘
       │
       ├──► /api/* → Flask (Gunicorn)
       │
       └──► /* → Static files (Vite build)
```

- **Web Server**: Nginx
- **Application Server**: Gunicorn (Flask)
- **Database**: PostgreSQL
- **Session Store**: Redis
- **Static Assets**: Served by Nginx or CDN

## Future Enhancements

- [ ] User bookmarks
- [ ] Progress tracking
- [ ] Material categories/filtering
- [ ] Search functionality
- [ ] Admin dashboard
- [ ] Email notifications
- [ ] File uploads
- [ ] Material versioning
- [ ] Comments/discussions
- [ ] Real-time updates (WebSockets)

## References

- [Vue.js Documentation](https://vuejs.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://www.sqlalchemy.org/)
- [TailwindCSS Documentation](https://tailwindcss.com/)
- [Notion API Documentation](https://developers.notion.com/)
