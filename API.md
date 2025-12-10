# API Documentation

This document describes all API endpoints available in the StudyHall Platform backend.

## Base URL

- **Development**: `http://localhost:5000`
- **Production**: Configure based on deployment

All API endpoints are prefixed with `/api/`.

## Authentication

The API uses session-based authentication with HTTP-only cookies. After successful login or registration, a `session_token` cookie is set, which should be included in subsequent requests.

### Session Management

- Sessions are stored in-memory (upgrade to Redis for production)
- Session tokens expire after 7 days (604800 seconds)
- Sessions are validated on protected endpoints

## Endpoints

### Authentication

#### POST `/api/auth/login`

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

**Cookies Set:**
- `session_token`: HTTP-only cookie with session token

---

#### POST `/api/auth/register`

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

or

```json
{
  "error": "Maximum of 30 students reached"
}
```

**Notes:**
- Maximum of 30 students allowed (hardcoded limit)
- Email must be unique
- Password is hashed using SHA-256 (upgrade to bcrypt for production)

**Cookies Set:**
- `session_token`: HTTP-only cookie with session token

---

#### POST `/api/auth/logout`

Logout the current user and invalidate their session.

**Request:** No body required

**Response (200 OK):**
```json
{
  "success": true
}
```

**Cookies Deleted:**
- `session_token`: Removed from client

---

#### GET `/api/auth/me`

Get the current authenticated student's information.

**Request:** No body required (uses session cookie)

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

#### GET `/api/materials`

Get a list of all course materials.

**Request:** No body required (requires authentication)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Introduction to Python",
    "content": "Python is a high-level programming language...",
    "category": "Python",
    "notion_url": "https://notion.so/...",
    "created_at": "2024-01-15T10:30:00"
  },
  {
    "id": 2,
    "title": "Variables and Data Types",
    "content": "Variables store data...",
    "category": "Python",
    "notion_url": null,
    "created_at": "2024-01-16T14:20:00"
  }
]
```

**Response (401 Unauthorized):**
```json
{
  "error": "Not authenticated"
}
```

**Notes:**
- Materials are ordered by `order_index` and `created_at`
- `notion_url` may be `null` if material was created manually

---

#### GET `/api/materials/<material_id>`

Get detailed information about a specific material.

**URL Parameters:**
- `material_id` (integer): The ID of the material

**Request:** No body required (requires authentication)

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Introduction to Python",
  "content": "Python is a high-level programming language...",
  "category": "Python",
  "notion_url": "https://notion.so/...",
  "created_at": "2024-01-15T10:30:00"
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Not authenticated"
}
```

**Response (404 Not Found):**
```json
{
  "error": "Material not found"
}
```

---

#### POST `/api/materials/sync-notion`

Sync materials from a Notion database.

**Request:** No body required (requires authentication)

**Response (200 OK):**
```json
{
  "success": true,
  "synced": 5
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Not authenticated"
}
```

**Response (500 Internal Server Error):**
```json
{
  "error": "Error message describing what went wrong"
}
```

**Notes:**
- Requires `NOTION_API_KEY` and `NOTION_DATABASE_ID` environment variables
- Fetches pages from the configured Notion database
- Only creates new materials (does not update existing ones)
- Uses `notion_page_id` to prevent duplicates
- If a page already exists (by `notion_page_id`), it is skipped

**Environment Variables Required:**
```bash
export NOTION_API_KEY="secret_..."
export NOTION_DATABASE_ID="..."
```

---

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
Invalid request data or validation errors.

```json
{
  "error": "Error message"
}
```

### 401 Unauthorized
Authentication required or invalid session.

```json
{
  "error": "Not authenticated"
}
```

### 404 Not Found
Resource not found.

```json
{
  "error": "Resource not found"
}
```

### 500 Internal Server Error
Server-side error.

```json
{
  "error": "Error message"
}
```

---

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:5173` (Frontend dev server)
- `http://localhost:5000` (Backend)

For production, update CORS origins in `backend/main.py`.

---

## Rate Limiting

Currently, there is no rate limiting implemented. Consider adding rate limiting for production deployments.

---

## Security Considerations

1. **Password Hashing**: Currently uses SHA-256. **Upgrade to bcrypt** for production.
2. **Session Storage**: In-memory sessions. **Upgrade to Redis** for production scalability.
3. **CORS**: Configure appropriate origins for production.
4. **Secret Key**: Change `SECRET_KEY` environment variable in production.
5. **HTTPS**: Always use HTTPS in production.

---

## Testing

API endpoints can be tested using:

- **cURL**:
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"student@studyhall.com","password":"password123"}' \
  -c cookies.txt

curl http://localhost:5000/api/materials -b cookies.txt
```

- **Postman**: Import the endpoints and configure cookie handling
- **Frontend**: Use `fetch()` with `credentials: 'include'` to handle cookies automatically

---

## Future Enhancements

- [ ] Add pagination for materials list
- [ ] Add filtering and search for materials
- [ ] Add bookmark endpoints
- [ ] Add progress tracking endpoints
- [ ] Add material update/delete endpoints
- [ ] Add rate limiting
- [ ] Add request validation middleware
- [ ] Add API versioning
