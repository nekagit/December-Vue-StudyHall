# API Documentation

Complete API reference for the StudyHall Platform backend.

## Base URL

- **Development**: `http://localhost:5000`
- **Production**: Configure based on deployment

All API endpoints are prefixed with `/api`.

## Authentication

The API uses session-based authentication. After successful login, a session token is stored in an HTTP-only cookie named `session_token`.

### Authentication Flow

1. User logs in via `POST /api/auth/login`
2. Server sets `session_token` cookie
3. Subsequent requests automatically include the cookie
4. Server validates the session token on protected endpoints

## Endpoints

### Authentication

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "student@studyhall.com",
  "password": "password123"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "student": {
    "id": 1,
    "email": "student@studyhall.com",
    "name": "Student Name"
  }
}
```

**Error Response** (401 Unauthorized):
```json
{
  "error": "Invalid email or password"
}
```

#### Register
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "newstudent@studyhall.com",
  "name": "New Student",
  "password": "password123"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "student": {
    "id": 2,
    "email": "newstudent@studyhall.com",
    "name": "New Student"
  }
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "Email already registered" // or "Maximum 30 students allowed"
}
```

#### Logout
```http
POST /api/auth/logout
```

**Response** (200 OK):
```json
{
  "success": true
}
```

#### Get Current User
```http
GET /api/auth/me
```

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "student@studyhall.com",
  "name": "Student Name"
}
```

**Error Response** (401 Unauthorized):
```json
{
  "error": "Not authenticated"
}
```

### Materials

#### List Materials
```http
GET /api/materials?search=python&category=Python
```

**Query Parameters**:
- `search` (optional): Search term for title and content
- `category` (optional): Filter by category

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Introduction to Python",
    "content": "Python is a programming language...",
    "category": "Python",
    "notion_url": "https://notion.so/...",
    "created_at": "2024-01-01T00:00:00",
    "progress": {
      "is_completed": false,
      "progress_percentage": 50,
      "last_accessed_at": "2024-01-15T10:30:00"
    },
    "is_bookmarked": true
  }
]
```

#### Get Material Categories
```http
GET /api/materials/categories
```

**Response** (200 OK):
```json
["Python", "Web Development", "Data Science"]
```

#### Get Material Detail
```http
GET /api/materials/:id
```

**Response** (200 OK):
```json
{
  "id": 1,
  "title": "Introduction to Python",
  "content": "Full content here...",
  "category": "Python",
  "notion_url": "https://notion.so/...",
  "created_at": "2024-01-01T00:00:00",
  "progress": {
    "is_completed": false,
    "progress_percentage": 50,
    "last_accessed_at": "2024-01-15T10:30:00"
  },
  "is_bookmarked": true
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "Material not found"
}
```

#### Sync from Notion
```http
POST /api/materials/sync-notion
```

**Response** (200 OK):
```json
{
  "success": true,
  "synced": 5
}
```

**Error Response** (500 Internal Server Error):
```json
{
  "error": "Notion API error: ..."
}
```

**Note**: Requires `NOTION_API_KEY` and `NOTION_DATABASE_ID` environment variables.

### Progress Tracking

#### Update Progress
```http
POST /api/progress/:material_id
Content-Type: application/json

{
  "is_completed": true,
  "progress_percentage": 100
}
```

**Request Body** (all fields optional):
- `is_completed` (boolean): Mark material as completed
- `progress_percentage` (number, 0-100): Set progress percentage

**Response** (200 OK):
```json
{
  "success": true,
  "progress": {
    "is_completed": true,
    "progress_percentage": 100,
    "last_accessed_at": "2024-01-15T10:30:00",
    "completed_at": "2024-01-15T10:30:00"
  }
}
```

### Bookmarks

#### List Bookmarks
```http
GET /api/bookmarks
```

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "title": "Introduction to Python",
    "content": "Python is a programming language...",
    "category": "Python",
    "notion_url": "https://notion.so/...",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### Add Bookmark
```http
POST /api/bookmarks/:material_id
```

**Response** (200 OK):
```json
{
  "success": true
}
```

**Error Response** (404 Not Found):
```json
{
  "error": "Material not found"
}
```

#### Remove Bookmark
```http
DELETE /api/bookmarks/:material_id
```

**Response** (200 OK):
```json
{
  "success": true
}
```

### Profile

#### Get Profile
```http
GET /api/profile
```

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "student@studyhall.com",
  "name": "Student Name",
  "created_at": "2024-01-01T00:00:00",
  "stats": {
    "total_materials": 50,
    "completed_materials": 25,
    "bookmarks_count": 10,
    "completion_rate": 50.0
  }
}
```

#### Update Profile
```http
PUT /api/profile
Content-Type: application/json

{
  "name": "Updated Name",
  "email": "newemail@studyhall.com",
  "password": "newpassword123"
}
```

**Request Body** (all fields optional):
- `name` (string): Update student name
- `email` (string): Update email address
- `password` (string): Update password

**Response** (200 OK):
```json
{
  "success": true,
  "student": {
    "id": 1,
    "email": "newemail@studyhall.com",
    "name": "Updated Name"
  }
}
```

**Error Response** (400 Bad Request):
```json
{
  "error": "Email already taken"
}
```

### Dashboard

#### Get Dashboard Stats
```http
GET /api/dashboard/stats
```

**Response** (200 OK):
```json
{
  "total_materials": 50,
  "completed_materials": 25,
  "in_progress_materials": 10,
  "not_started_materials": 15,
  "bookmarks_count": 10,
  "completion_rate": 50.0,
  "recent_activity": [
    {
      "id": 1,
      "title": "Introduction to Python",
      "category": "Python",
      "progress_percentage": 75,
      "is_completed": false,
      "last_accessed_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### Testing

#### Run Backend Tests
```http
POST /api/tests/backend/run
```

**Response** (200 OK):
```json
{
  "success": true,
  "tests_run": 25,
  "tests_passed": 24,
  "tests_failed": 1,
  "duration": 2.5
}
```

#### Get Backend Coverage
```http
GET /api/tests/backend/coverage
```

**Response** (200 OK):
```json
{
  "total_coverage": 85.5,
  "files": [
    {
      "name": "backend/models/student.py",
      "coverage": 90.0
    }
  ]
}
```

#### Run Frontend Tests
```http
POST /api/tests/frontend/run
```

**Response** (200 OK):
```json
{
  "success": true,
  "tests_run": 15,
  "tests_passed": 15,
  "tests_failed": 0,
  "duration": 1.2
}
```

#### Get Frontend Coverage
```http
GET /api/tests/frontend/coverage
```

**Response** (200 OK):
```json
{
  "total_coverage": 78.3,
  "files": [
    {
      "name": "src/views/Login.vue",
      "coverage": 85.0
    }
  ]
}
```

#### Get Tests Summary
```http
GET /api/tests/summary
```

**Response** (200 OK):
```json
{
  "backend": {
    "coverage": {
      "total_coverage": 85.5,
      "files": [...]
    }
  },
  "frontend": {
    "coverage": {
      "total_coverage": 78.3,
      "files": [...]
    }
  }
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Error message describing what went wrong"
}
```

### 401 Unauthorized
```json
{
  "error": "Not authenticated"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error message"
}
```

## Rate Limiting

Currently, there is no rate limiting implemented. Consider adding rate limiting for production deployments.

## CORS

CORS is enabled for:
- `http://localhost:5173` (frontend dev server)
- `http://localhost:5000` (backend)

Update CORS origins in `backend/main.py` for production.

## Environment Variables

Required environment variables:

- `SECRET_KEY`: Secret key for Flask sessions (default: "dev-secret-key-change-in-production")
- `NOTION_API_KEY`: Notion API key (optional, for Notion sync)
- `NOTION_DATABASE_ID`: Notion database ID (optional, for Notion sync)
