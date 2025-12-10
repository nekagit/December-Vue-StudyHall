# API Documentation

Complete reference for all API endpoints in the StudyHall Platform.

## Base URL

- **Development**: `http://localhost:5000`
- **Production**: Configure based on your deployment

All endpoints are prefixed with `/api`.

## Authentication

Most endpoints require authentication via session cookies. The session token is set as an HTTP-only cookie after login.

### Session Management

- Sessions are stored in-memory (MVP)
- Session token is set as `session_token` cookie
- Sessions expire after 7 days (604800 seconds)

---

## Authentication Endpoints

### POST /api/auth/login

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

**Sets Cookie:** `session_token` (HTTP-only, 7-day expiry)

---

### POST /api/auth/register

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
  "error": "Maximum of 30 students reached"
}
```
or
```json
{
  "error": "Email already registered"
}
```

**Limitations:**
- Maximum 30 students allowed
- Email must be unique

---

### POST /api/auth/logout

Logout the current user and invalidate session.

**Response (200 OK):**
```json
{
  "success": true
}
```

**Deletes Cookie:** `session_token`

---

### GET /api/auth/me

Get the currently authenticated user.

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

## Materials Endpoints

### GET /api/materials

Get all materials with optional filtering and search.

**Query Parameters:**
- `search` (optional) - Search in title and content
- `category` (optional) - Filter by category

**Example:**
```
GET /api/materials?search=python&category=Basics
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Introduction to Python",
    "content": "Python is a programming language...",
    "category": "Basics",
    "notion_url": "https://notion.so/...",
    "created_at": "2024-01-01T00:00:00",
    "progress": {
      "is_completed": false,
      "progress_percentage": 45,
      "last_accessed_at": "2024-01-15T10:30:00"
    },
    "is_bookmarked": true
  }
]
```

**Response (401 Unauthorized):**
```json
{
  "error": "Not authenticated"
}
```

---

### GET /api/materials/:id

Get a specific material by ID.

**Path Parameters:**
- `id` (integer) - Material ID

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Introduction to Python",
  "content": "Python is a programming language...",
  "category": "Basics",
  "notion_url": "https://notion.so/...",
  "created_at": "2024-01-01T00:00:00",
  "progress": {
    "is_completed": false,
    "progress_percentage": 45,
    "last_accessed_at": "2024-01-15T10:30:00"
  },
  "is_bookmarked": true
}
```

**Response (404 Not Found):**
```json
{
  "error": "Material not found"
}
```

**Note:** This endpoint automatically updates `last_accessed_at` when accessed.

---

### GET /api/materials/categories

Get all unique categories from materials.

**Response (200 OK):**
```json
["Basics", "Advanced", "Web Development", "Data Science"]
```

---

### POST /api/materials/sync-notion

Sync materials from Notion database.

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

**Requirements:**
- `NOTION_API_KEY` environment variable must be set
- `NOTION_DATABASE_ID` environment variable must be set
- Notion database must be shared with the integration

---

## Progress Endpoints

### POST /api/progress/:id

Create or update progress for a material.

**Path Parameters:**
- `id` (integer) - Material ID

**Request Body:**
```json
{
  "is_completed": true,
  "progress_percentage": 100
}
```

**Fields:**
- `is_completed` (boolean, optional) - Mark as completed
- `progress_percentage` (integer, optional) - Progress percentage (0-100)

**Response (200 OK):**
```json
{
  "success": true,
  "progress": {
    "is_completed": true,
    "progress_percentage": 100,
    "last_accessed_at": "2024-01-15T10:30:00",
    "completed_at": "2024-01-15T10:35:00"
  }
}
```

**Note:**
- Setting `is_completed: true` automatically sets `progress_percentage` to 100
- Setting `progress_percentage: 100` automatically sets `is_completed: true`
- Progress percentage is clamped between 0 and 100

---

### PUT /api/progress/:id

Same as POST /api/progress/:id (alias for update).

---

## Bookmark Endpoints

### GET /api/bookmarks

Get all bookmarked materials for the current user.

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Introduction to Python",
    "content": "Python is a programming language...",
    "category": "Basics",
    "notion_url": "https://notion.so/...",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

### POST /api/bookmarks/:id

Add a material to bookmarks.

**Path Parameters:**
- `id` (integer) - Material ID

**Response (200 OK):**
```json
{
  "success": true
}
```

**Response (404 Not Found):**
```json
{
  "error": "Material not found"
}
```

**Note:** If already bookmarked, returns success without error.

---

### DELETE /api/bookmarks/:id

Remove a material from bookmarks.

**Path Parameters:**
- `id` (integer) - Material ID

**Response (200 OK):**
```json
{
  "success": true
}
```

---

## Profile Endpoints

### GET /api/profile

Get user profile with statistics.

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "student@studyhall.com",
  "name": "John Doe",
  "created_at": "2024-01-01T00:00:00",
  "stats": {
    "total_materials": 50,
    "completed_materials": 15,
    "bookmarks_count": 8,
    "completion_rate": 30.0
  }
}
```

---

### PUT /api/profile

Update user profile.

**Request Body:**
```json
{
  "name": "John Updated",
  "email": "newemail@studyhall.com",
  "password": "newpassword"
}
```

**Fields:**
- `name` (string, optional) - Update name
- `email` (string, optional) - Update email (must be unique)
- `password` (string, optional) - Update password

**Response (200 OK):**
```json
{
  "success": true,
  "student": {
    "id": 1,
    "email": "newemail@studyhall.com",
    "name": "John Updated"
  }
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Email already taken"
}
```

---

## Dashboard Endpoints

### GET /api/dashboard/stats

Get dashboard statistics and recent activity.

**Response (200 OK):**
```json
{
  "total_materials": 50,
  "completed_materials": 15,
  "in_progress_materials": 10,
  "not_started_materials": 25,
  "bookmarks_count": 8,
  "completion_rate": 30.0,
  "recent_activity": [
    {
      "id": 1,
      "title": "Introduction to Python",
      "category": "Basics",
      "progress_percentage": 45,
      "is_completed": false,
      "last_accessed_at": "2024-01-15T10:30:00"
    }
  ]
}
```

**Fields:**
- `total_materials` - Total number of materials
- `completed_materials` - Number of completed materials
- `in_progress_materials` - Number of materials with progress > 0% but not completed
- `not_started_materials` - Number of materials not yet started
- `bookmarks_count` - Number of bookmarked materials
- `completion_rate` - Percentage of completed materials
- `recent_activity` - Last 5 accessed materials

---

## Error Responses

All endpoints may return the following error responses:

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
  "error": "Error message"
}
```

---

## Rate Limiting

Currently, there is no rate limiting implemented. Consider adding rate limiting for production use.

## CORS

CORS is enabled for:
- `http://localhost:5173` (frontend dev server)
- `http://localhost:5000` (backend)

Configure CORS properly for production deployment.

---

## Example Usage

### JavaScript/Fetch Example

```javascript
// Login
const response = await fetch('http://localhost:5000/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include', // Important for cookies
  body: JSON.stringify({
    email: 'student@studyhall.com',
    password: 'password123'
  })
});

const data = await response.json();

// Get materials
const materialsResponse = await fetch('http://localhost:5000/api/materials', {
  credentials: 'include'
});

const materials = await materialsResponse.json();
```

### cURL Example

```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@studyhall.com","password":"password123"}' \
  -c cookies.txt

# Get materials (using saved cookies)
curl http://localhost:5000/api/materials \
  -b cookies.txt
```
