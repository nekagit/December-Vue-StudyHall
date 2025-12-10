# Architecture Documentation

Comprehensive architecture overview of the StudyHall Platform.

## System Overview

StudyHall is a modern Single Page Application (SPA) learning platform designed for managing course materials for up to 30 students. It features Python course content, a browser-based Python compiler, and Notion integration.

## High-Level Architecture

```
┌─────────────────┐
│   Web Browser   │
│   (Vue.js SPA)  │
└────────┬────────┘
         │ HTTP/HTTPS
         │ (REST API)
         ▼
┌─────────────────┐
│  Flask Backend  │
│   (Python API)  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────┐
│ SQLite │ │  Notion  │
│   DB   │ │    API   │
└────────┘ └──────────┘
```

## Technology Stack

### Backend
- **Framework**: Flask (minimal REST API)
- **ORM**: SQLAlchemy
- **Database**: SQLite (MVP, upgradeable to PostgreSQL)
- **Authentication**: Session-based with HTTP-only cookies
- **CORS**: Enabled for frontend development

### Frontend
- **Framework**: Vue.js 3 (Composition API)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **Build Tool**: Vite
- **Routing**: Vue Router
- **Python Execution**: Pyodide (browser-based)

## Project Structure

```
December-Vue-StudyHall/
├── backend/
│   ├── main.py              # Flask application entry point
│   ├── database.py          # SQLAlchemy database configuration
│   ├── init_db.py           # Database initialization script
│   ├── requirements.txt     # Python dependencies
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── student.py       # Student model
│   │   ├── material.py      # Material model
│   │   ├── bookmark.py      # Bookmark model
│   │   └── progress.py      # Progress tracking model
│   └── services/            # Business logic layer
│       ├── auth.py          # Authentication service
│       ├── session.py       # Session management
│       └── notion_sync.py   # Notion integration service
│
├── frontend/
│   ├── src/
│   │   ├── main.ts          # Application entry point
│   │   ├── App.vue          # Root component
│   │   ├── style.scss       # TailwindCSS imports
│   │   ├── views/           # Page-level components
│   │   │   ├── Home.vue
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── Materials.vue
│   │   │   ├── MaterialDetail.vue
│   │   │   └── Compiler.vue
│   │   ├── components/      # Reusable components
│   │   │   ├── PythonRunner.vue
│   │   │   └── HelloWorld.vue
│   │   └── utils/           # Utility functions
│   │       └── mount.ts
│   ├── vite.config.ts       # Vite configuration
│   ├── package.json         # Node.js dependencies
│   └── index.html           # HTML entry point
│
├── manage.py                # Management script
└── README.md                # Project documentation
```

## Backend Architecture

### Flask Application (`backend/main.py`)

The Flask application follows a minimal REST API pattern:

- **No templates**: Backend only serves JSON responses
- **Session management**: Uses Flask sessions and HTTP-only cookies
- **Database sessions**: Uses SQLAlchemy session management
- **CORS**: Configured for frontend development

### Database Layer (`backend/database.py`)

- Uses SQLAlchemy ORM
- SQLite database for MVP
- Session management via `SessionLocal`
- Base class for all models

### Models (`backend/models/`)

#### Student Model
- Stores student information
- Email uniqueness constraint
- Password hashing (SHA-256 for MVP, should use bcrypt in production)
- Active status flag

#### Material Model
- Course content storage
- Notion integration fields (`notion_page_id`, `notion_url`)
- Category and ordering support
- Timestamps for creation and updates

#### Bookmark Model
- Many-to-one relationship with Student
- Many-to-one relationship with Material
- Tracks when materials are bookmarked

#### Progress Model
- Tracks student progress through materials
- Status: `not_started`, `in_progress`, `completed`
- Progress percentage (0-100)
- Timestamps for access and completion

### Services Layer (`backend/services/`)

#### Auth Service (`auth.py`)
- Password hashing and verification
- Student authentication
- Student creation with validation (30 student limit)

#### Session Service (`session.py`)
- In-memory session storage (MVP)
- Session token generation
- Session validation and deletion
- **Note**: Should be upgraded to Redis for production

#### Notion Sync Service (`notion_sync.py`)
- Async Notion API integration
- Fetches pages from Notion database
- Syncs content to local database

## Frontend Architecture

### Vue.js Application Structure

#### Entry Point (`main.ts`)
- Initializes Vue app
- Configures Vue Router
- Sets up authentication guards
- Mounts root component

#### Routing (`main.ts`)
- Client-side routing with Vue Router
- Protected routes with `requiresAuth` meta
- Authentication guard checks for session token

#### Components

**Views (Pages):**
- `Home.vue`: Landing page
- `Login.vue`: Authentication form
- `Register.vue`: Registration form
- `Materials.vue`: Material listing with search/filter
- `MaterialDetail.vue`: Individual material view
- `Compiler.vue`: Python code execution interface

**Reusable Components:**
- `PythonRunner.vue`: Pyodide-based Python execution component

### Styling

- **TailwindCSS**: Utility-first CSS framework
- **Responsive Design**: Mobile-first approach
- **Color Scheme**: Indigo primary colors

### State Management

Currently uses:
- Component-level state (Composition API `ref`/`reactive`)
- Cookie-based session storage
- API calls for data fetching

**Future Consideration**: May benefit from Pinia for global state management as the app grows.

## Data Flow

### Authentication Flow

```
1. User submits login form
2. Frontend sends POST /api/auth/login
3. Backend validates credentials
4. Backend creates session token
5. Backend sets HTTP-only cookie
6. Frontend receives success response
7. Frontend redirects to protected route
8. Router guard validates cookie on route changes
```

### Material Fetching Flow

```
1. User navigates to /materials
2. Component mounts and calls GET /api/materials
3. Backend queries database
4. Backend includes bookmark status for current user
5. Frontend receives and displays materials
6. User can search/filter (client-side or server-side)
```

### Notion Sync Flow

```
1. User clicks "Sync from Notion"
2. Frontend sends POST /api/materials/sync-notion
3. Backend calls Notion API (async)
4. Backend processes pages
5. Backend creates/updates materials in database
6. Frontend receives sync count
7. Frontend refreshes material list
```

## API Design

### RESTful Principles

- **Resources**: Materials, Bookmarks, Progress, Students
- **HTTP Methods**: GET (read), POST (create), PUT (update), DELETE (delete)
- **Status Codes**: 200 (success), 201 (created), 400 (bad request), 401 (unauthorized), 404 (not found), 500 (server error)
- **JSON**: All requests and responses use JSON

### Endpoint Patterns

- `/api/auth/*` - Authentication endpoints
- `/api/materials/*` - Material management
- `/api/bookmarks/*` - Bookmark management
- `/api/progress/*` - Progress tracking
- `/api/dashboard/*` - Dashboard data

## Security Considerations

### Current Implementation (MVP)

- **Password Hashing**: SHA-256 (should upgrade to bcrypt)
- **Session Management**: In-memory (should upgrade to Redis)
- **CORS**: Configured for development origins
- **HTTP-only Cookies**: Prevents XSS attacks
- **SQL Injection**: Protected by SQLAlchemy ORM

### Production Recommendations

1. **Password Security**: Use bcrypt with salt rounds
2. **Session Storage**: Redis or database-backed sessions
3. **HTTPS**: Enforce HTTPS in production
4. **Rate Limiting**: Add rate limiting to prevent abuse
5. **Input Validation**: Add comprehensive input validation
6. **SQL Injection**: Already protected by ORM, but validate all inputs
7. **XSS Protection**: Vue.js automatically escapes content
8. **CSRF Protection**: Consider adding CSRF tokens

## Database Schema

### Relationships

```
Student (1) ──< (Many) Bookmark
Student (1) ──< (Many) Progress
Material (1) ──< (Many) Bookmark
Material (1) ──< (Many) Progress
```

### Key Constraints

- Student email must be unique
- Material notion_page_id must be unique
- Bookmark (student_id, material_id) should be unique (enforced in application logic)

## Development Workflow

### Local Development

1. Backend runs on `http://localhost:5000`
2. Frontend dev server runs on `http://localhost:5173`
3. Frontend proxies `/api/*` requests to backend
4. Use `./manage.py dev` to run both servers

### Build Process

1. Frontend TypeScript compilation (`vue-tsc`)
2. Vite build process
3. Static assets generation
4. Backend serves static files in production

## Deployment Architecture

### MVP Deployment

- **Backend**: Single Flask server
- **Frontend**: Static files served by Flask
- **Database**: SQLite file
- **Session Storage**: In-memory

### Production Deployment Recommendations

- **Backend**: WSGI server (Gunicorn) behind reverse proxy (Nginx)
- **Frontend**: CDN or Nginx static file serving
- **Database**: PostgreSQL with connection pooling
- **Session Storage**: Redis
- **Load Balancing**: Multiple backend instances
- **Monitoring**: Application performance monitoring
- **Logging**: Centralized logging system

## Scalability Considerations

### Current Limitations

- 30 student hard limit
- In-memory session storage
- SQLite database (single writer)
- Single-threaded Flask development server

### Scaling Strategies

1. **Remove Student Limit**: Make configurable or remove entirely
2. **Database**: Migrate to PostgreSQL for concurrent access
3. **Session Storage**: Use Redis cluster
4. **Backend**: Use Gunicorn with multiple workers
5. **Caching**: Add Redis caching layer
6. **CDN**: Use CDN for static assets
7. **Horizontal Scaling**: Multiple backend instances with load balancer

## Integration Points

### Notion API Integration

- **Authentication**: API key via environment variable
- **Database ID**: Notion database ID via environment variable
- **Sync Process**: Manual trigger via API endpoint
- **Future**: Could add scheduled syncs or webhooks

### Pyodide Integration

- **Browser-based**: Runs entirely in browser
- **No Backend**: Python execution happens client-side
- **Limitations**: No file system access, network restrictions
- **Use Case**: Educational Python code execution

## Future Enhancements

1. **Real-time Updates**: WebSocket support for live updates
2. **File Uploads**: Support for material file attachments
3. **Rich Text Editor**: WYSIWYG editor for material content
4. **Comments/Discussions**: Student discussion threads
5. **Analytics**: Learning analytics and progress tracking
6. **Mobile App**: Native mobile application
7. **Offline Support**: Service workers for offline access
8. **Multi-tenancy**: Support for multiple courses/organizations
