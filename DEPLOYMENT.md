# Deployment Guide

Guide for deploying the StudyHall Platform to production.

## Table of Contents

- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Environment Configuration](#environment-configuration)
- [Backend Deployment](#backend-deployment)
- [Frontend Deployment](#frontend-deployment)
- [Database Setup](#database-setup)
- [Security Considerations](#security-considerations)
- [Deployment Options](#deployment-options)
- [Monitoring](#monitoring)

## Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All environment variables are set
- [ ] Database is migrated and backed up
- [ ] Frontend is built for production
- [ ] CORS is configured for production domain
- [ ] Secret key is changed from default
- [ ] Password hashing is upgraded (bcrypt recommended)
- [ ] Session storage is configured (Redis recommended)
- [ ] SSL/TLS certificates are configured
- [ ] Error logging is set up
- [ ] Rate limiting is configured

## Environment Configuration

### Required Environment Variables

**Backend:**
```bash
# Flask
SECRET_KEY=your-production-secret-key-min-32-chars
FLASK_ENV=production

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Notion Integration (optional)
NOTION_API_KEY=your-notion-api-key
NOTION_DATABASE_ID=your-database-id

# Session Storage (if using Redis)
REDIS_URL=redis://localhost:6379/0
```

**Frontend:**
- No environment variables needed (build-time configuration)

### Setting Environment Variables

**Linux/macOS:**
```bash
export SECRET_KEY="your-secret-key"
export DATABASE_URL="postgresql://..."
```

**Docker:**
```dockerfile
ENV SECRET_KEY=your-secret-key
ENV DATABASE_URL=postgresql://...
```

**Platform-specific:**
- Heroku: `heroku config:set SECRET_KEY=your-key`
- AWS: Use Systems Manager Parameter Store
- Vercel: Use environment variables in dashboard

## Backend Deployment

### Option 1: Traditional Server (Gunicorn)

1. **Install Gunicorn:**
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn config:**
   ```python
   # gunicorn_config.py
   bind = "0.0.0.0:5000"
   workers = 4
   worker_class = "sync"
   timeout = 120
   ```

3. **Run with Gunicorn:**
   ```bash
   gunicorn -c gunicorn_config.py backend.main:app
   ```

4. **Use systemd service (Linux):**
   ```ini
   # /etc/systemd/system/studyhall.service
   [Unit]
   Description=StudyHall Backend
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/December-Vue-StudyHall
   Environment="PATH=/path/to/venv/bin"
   ExecStart=/path/to/venv/bin/gunicorn -c gunicorn_config.py backend.main:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable studyhall
   sudo systemctl start studyhall
   ```

### Option 2: Docker

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY backend/requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   RUN pip install gunicorn

   COPY backend/ ./backend/
   COPY manage.py .

   ENV PYTHONPATH=/app
   ENV FLASK_APP=backend.main:app

   EXPOSE 5000

   CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.main:app"]
   ```

2. **Build and run:**
   ```bash
   docker build -t studyhall-backend .
   docker run -p 5000:5000 \
     -e SECRET_KEY=your-key \
     -e DATABASE_URL=postgresql://... \
     studyhall-backend
   ```

### Option 3: Platform-as-a-Service

#### Heroku

1. **Create `Procfile`:**
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT backend.main:app
   ```

2. **Create `runtime.txt`:**
   ```
   python-3.11.0
   ```

3. **Deploy:**
   ```bash
   heroku create studyhall-backend
   heroku config:set SECRET_KEY=your-key
   git push heroku main
   ```

#### Railway

1. **Create `railway.json`:**
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "gunicorn -w 4 -b 0.0.0.0:$PORT backend.main:app",
       "restartPolicyType": "ON_FAILURE"
     }
   }
   ```

2. **Deploy via Railway dashboard**

## Frontend Deployment

### Build for Production

```bash
cd frontend
npm run build
```

This creates optimized files in `frontend/dist/`.

### Option 1: Static Hosting (Recommended)

#### Vercel

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Create `vercel.json`:**
   ```json
   {
     "builds": [
       {
         "src": "frontend/package.json",
         "use": "@vercel/static-build",
         "config": {
           "distDir": "dist"
         }
       }
     ],
     "routes": [
       {
         "src": "/api/(.*)",
         "dest": "https://your-backend-url.com/api/$1"
       },
       {
         "src": "/(.*)",
         "dest": "/frontend/dist/$1"
       }
     ]
   }
   ```

3. **Deploy:**
   ```bash
   vercel
   ```

#### Netlify

1. **Create `netlify.toml`:**
   ```toml
   [build]
     command = "cd frontend && npm run build"
     publish = "frontend/dist"

   [[redirects]]
     from = "/api/*"
     to = "https://your-backend-url.com/api/:splat"
     status = 200
     force = true
   ```

2. **Deploy via Netlify dashboard**

#### AWS S3 + CloudFront

1. **Build frontend:**
   ```bash
   cd frontend && npm run build
   ```

2. **Upload to S3:**
   ```bash
   aws s3 sync frontend/dist s3://your-bucket-name
   ```

3. **Configure CloudFront** for CDN and HTTPS

### Option 2: Serve with Backend

If serving frontend from Flask:

1. **Update `main.py`:**
   ```python
   from flask import send_from_directory
   import os

   @app.route('/', defaults={'path': ''})
   @app.route('/<path:path>')
   def serve_frontend(path):
       if path and os.path.exists(os.path.join('frontend/dist', path)):
           return send_from_directory('frontend/dist', path)
       return send_from_directory('frontend/dist', 'index.html')
   ```

2. **Serve static files:**
   ```python
   app.static_folder = 'frontend/dist'
   ```

### Option 3: Docker

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Database Setup

### SQLite (MVP - Not Recommended for Production)

SQLite works for MVP but has limitations:
- No concurrent writes
- No network access
- Limited scalability

### PostgreSQL (Recommended)

1. **Install PostgreSQL:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql

   # macOS
   brew install postgresql
   ```

2. **Create database:**
   ```sql
   CREATE DATABASE studyhall;
   CREATE USER studyhall_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE studyhall TO studyhall_user;
   ```

3. **Update `database.py`:**
   ```python
   SQLALCHEMY_DATABASE_URL = os.getenv(
       "DATABASE_URL",
       "postgresql://studyhall_user:secure_password@localhost/studyhall"
   )
   ```

4. **Run migrations:**
   ```bash
   # Tables are auto-created, or use Alembic
   alembic upgrade head
   ```

### Database Migrations

Use Alembic for production migrations:

1. **Install Alembic:**
   ```bash
   pip install alembic
   ```

2. **Initialize:**
   ```bash
   alembic init alembic
   ```

3. **Configure `alembic/env.py`:**
   ```python
   from backend.database import Base
   target_metadata = Base.metadata
   ```

4. **Create migration:**
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

5. **Apply:**
   ```bash
   alembic upgrade head
   ```

## Security Considerations

### 1. Password Hashing

**Upgrade from SHA-256 to bcrypt:**

```python
# backend/services/auth.py
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())
```

### 2. Session Storage

**Upgrade to Redis:**

```python
# backend/services/session.py
import redis
import json

redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))

def create_session(student_id: int) -> str:
    token = secrets.token_urlsafe(32)
    redis_client.setex(
        f"session:{token}",
        604800,  # 7 days
        json.dumps({"student_id": student_id})
    )
    return token
```

### 3. CORS Configuration

**Update for production domain:**

```python
# backend/main.py
CORS(app, supports_credentials=True, origins=[
    "https://your-frontend-domain.com",
    "https://www.your-frontend-domain.com"
])
```

### 4. HTTPS

- Use reverse proxy (Nginx, Caddy)
- Configure SSL certificates (Let's Encrypt)
- Force HTTPS redirects

### 5. Rate Limiting

**Add Flask-Limiter:**

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/auth/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    # ...
```

### 6. Environment Variables

Never commit secrets. Use:
- Environment variables
- Secret management services (AWS Secrets Manager, HashiCorp Vault)
- `.env` files (not committed)

## Deployment Options

### Full Stack Deployment

#### Option 1: Separate Frontend/Backend

- **Backend**: Deploy to Heroku/Railway/AWS
- **Frontend**: Deploy to Vercel/Netlify
- **Database**: Managed PostgreSQL (AWS RDS, Heroku Postgres)

#### Option 2: Single Server

- **Backend + Frontend**: Deploy to single server
- **Reverse Proxy**: Nginx for routing
- **Database**: PostgreSQL on same server or managed

**Nginx Configuration:**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/studyhall
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=studyhall
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Monitoring

### Error Tracking

**Sentry:**

```python
# backend/main.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### Logging

**Structured Logging:**

```python
import logging
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)s %(levelname)s %(message)s'
)

logger = logging.getLogger(__name__)
```

### Health Checks

**Add health check endpoint:**

```python
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "database": check_database_connection()
    })
```

### Performance Monitoring

- Use APM tools (New Relic, Datadog)
- Monitor database query performance
- Track API response times
- Monitor frontend bundle size

## Post-Deployment

1. **Verify endpoints:**
   ```bash
   curl https://your-api.com/api/health
   ```

2. **Test authentication:**
   ```bash
   curl -X POST https://your-api.com/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@test.com","password":"test"}'
   ```

3. **Monitor logs:**
   ```bash
   # System logs
   journalctl -u studyhall -f

   # Application logs
   tail -f /var/log/studyhall/app.log
   ```

4. **Set up backups:**
   - Database backups (daily)
   - Configuration backups
   - SSL certificate backups

## Troubleshooting

### Common Issues

1. **502 Bad Gateway**: Backend not running or wrong port
2. **CORS Errors**: Check CORS configuration
3. **Database Connection**: Verify DATABASE_URL
4. **Static Files 404**: Check build output and nginx config

### Debugging Production

1. **Enable debug logging:**
   ```python
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check application logs:**
   ```bash
   tail -f /var/log/studyhall/app.log
   ```

3. **Test database connection:**
   ```python
   from backend.database import engine
   engine.connect()
   ```

## Scaling

### Horizontal Scaling

- Use load balancer (Nginx, AWS ALB)
- Multiple backend instances
- Shared session storage (Redis)
- Database connection pooling

### Vertical Scaling

- Increase server resources
- Optimize database queries
- Enable caching (Redis)
- CDN for static assets
