# API Documentation

Complete API reference for the StudyHall Platform backend.

## Base URL

- Development: `http://localhost:5000`
- Production: Configure based on deployment

All endpoints are prefixed with `/api/`.

## Authentication

The API uses session-based authentication with HTTP-only cookies. After successful login, a `session_token` cookie is set and must be included in subsequent requests.

### Authentication Flow

1. User logs in via `POST /api/auth/login`
2. Server sets `session_token` cookie
3. Client includes cookie automatically in subsequent requests
4. Server validates session token on protected endpoints

## Endpoints

### Authentication

#### `POST /api/auth/login`

Authenticate a student and create a session.

**Request Body:**
```json
{
  "email": "student@studyhall.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "student": {
    "id": 1,
    "email": "student@studyhall.com",
    "name": "John Doe"
  }
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Invalid email or password"
}
```

---

#### `POST /api/auth/register`

Register a new student account.

**Request Body:**
```json
{
  "email": "newstudent@studyhall.com",
  "name": "Jane Doe",
  "password": "securepassword"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "student": {
    "id": 2,
    "email": "newstudent@studyhall.com",
    "name": "Jane Doe"
  }
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Email already registered"
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Maximum of 30 students reached"
}
```

**Note:** The platform has a hard limit of 30 students.

---

#### `POST /api/auth/logout`

Logout the current user and invalidate session.

**Response (200 OK):**
```json
{
  "success": true
}
```

---

#### `GET /api/auth/me`

Get the current authenticated student's information.

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "student@studyhall.com",
  "name": "John Doe"
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Not authenticated"
}
```

---

### Materials

#### `GET /api/materials`

Get all materials with optional filtering and search.

**Query Parameters:**
- `search` (optional): Search term to filter by title or content
- `category` (optional): Filter by category name

**Example:**
```
GET /api/materials?search=python&category=Python
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Introduction to Python",
    "content": "Python is a programming language...",
    "category": "Python",
    "notion_url": "https://notion.so/...",
    "created_at": "2024-01-01T00:00:00",
    "is_bookmarked": true
  }
]
```

---

#### `GET /api/materials/:id`

Get detailed information about a specific material.

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Introduction to Python",
  "content": "Python is a programming language...",
  "category": "Python",
  "notion_url": "https://notion.so/...",
  "created_at": "2024-01-01T00:00:00",
  "is_bookmarked": true,
  "bookmark_id": 5,
  "progress": {
    "status": "in_progress",
    "progress_percentage": 45.0
  }
}
```

**Response (404 Not Found):**
```json
{
  "error": "Material not found"
}
```

---

#### `GET /api/materials/categories`

Get all available material categories.

**Response (200 OK):**
```json
["Python", "Web Development", "Data Science"]
```

---

#### `POST /api/materials/sync-notion`

Sync materials from Notion database.

**Requirements:**
- `NOTION_API_KEY` environment variable must be set
- `NOTION_DATABASE_ID` environment variable must be set
- Notion database must be shared with the integration

**Response (200 OK):**
```json
{
  "success": true,
  "synced": 5
}
```

**Response (500 Internal Server Error):**
```json
{
  "error": "Error message"
}
```

---

### Bookmarks

#### `GET /api/bookmarks`

Get all bookmarks for the current student.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "material_id": 5,
    "material": {
      "id": 5,
      "title": "Introduction to Python",
      "category": "Python",
      "created_at": "2024-01-01T00:00:00"
    },
    "created_at": "2024-01-02T00:00:00"
  }
]
```

---

#### `POST /api/bookmarks`

Create a new bookmark for a material.

**Request Body:**
```json
{
  "material_id": 5
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "bookmark": {
    "id": 1,
    "material_id": 5,
    "created_at": "2024-01-02T00:00:00"
  }
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Bookmark already exists"
}
```

---

#### `DELETE /api/bookmarks/:id`

Delete a bookmark by ID.

**Response (200 OK):**
```json
{
  "success": true
}
```

---

#### `DELETE /api/bookmarks/material/:material_id`

Delete a bookmark by material ID.

**Response (200 OK):**
```json
{
  "success": true
}
```

---

### Progress

#### `GET /api/progress`

Get all progress records for the current student.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "material_id": 5,
    "material": {
      "id": 5,
      "title": "Introduction to Python",
      "category": "Python"
    },
    "status": "in_progress",
    "progress_percentage": 45.0,
    "last_accessed_at": "2024-01-02T10:00:00",
    "completed_at": null
  }
]
```

---

#### `GET /api/progress/material/:material_id`

Get progress for a specific material.

**Response (200 OK):**
```json
{
  "id": 1,
  "material_id": 5,
  "status": "in_progress",
  "progress_percentage": 45.0,
  "last_accessed_at": "2024-01-02T10:00:00",
  "completed_at": null
}
```

**Response (200 OK) - No progress record:**
```json
{
  "material_id": 5,
  "status": "not_started",
  "progress_percentage": 0.0,
  "last_accessed_at": null,
  "completed_at": null
}
```

---

#### `POST /api/progress/material/:material_id`
#### `PUT /api/progress/material/:material_id`

Create or update progress for a material.

**Request Body:**
```json
{
  "status": "in_progress",
  "progress_percentage": 75.0
}
```

**Status Values:**
- `not_started`
- `in_progress`
- `completed`

**Progress Percentage:**
- Must be between 0 and 100

**Response (200 OK):**
```json
{
  "success": true,
  "progress": {
    "id": 1,
    "material_id": 5,
    "status": "in_progress",
    "progress_percentage": 75.0,
    "last_accessed_at": "2024-01-02T10:00:00",
    "completed_at": null
  }
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Invalid status"
}
```

---

### Dashboard

#### `GET /api/dashboard/stats`

Get dashboard statistics for the current student.

**Response (200 OK):**
```json
{
  "total_materials": 50,
  "total_bookmarks": 10,
  "completed_materials": 5,
  "in_progress_materials": 8,
  "recent_bookmarks": [
    {
      "id": 1,
      "material": {
        "id": 5,
        "title": "Introduction to Python",
        "category": "Python"
      },
      "created_at": "2024-01-02T00:00:00"
    }
  ],
  "recent_progress": [
    {
      "id": 1,
      "material": {
        "id": 5,
        "title": "Introduction to Python",
        "category": "Python"
      },
      "status": "in_progress",
      "progress_percentage": 45.0,
      "last_accessed_at": "2024-01-02T10:00:00"
    }
  ]
}
```

---

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

---

## CORS

The API supports CORS for the following origins:
- `http://localhost:5173` (Frontend dev server)
- `http://localhost:5000` (Backend)

Credentials are supported via cookies.

---

## Rate Limiting

Currently, there is no rate limiting implemented. Consider adding rate limiting for production deployments.

---

## Notes

- All timestamps are in ISO 8601 format
- All endpoints require authentication except `/api/auth/login` and `/api/auth/register`
- Session tokens expire after 7 days (604800 seconds)
- The platform has a hard limit of 30 students
