# Deployment Guide

Complete guide for deploying the StudyHall Platform to production.

## Overview

This guide covers deploying both the backend Flask API and frontend Vue.js application. The MVP uses SQLite, but production deployments should use PostgreSQL.

## Prerequisites

- Server with Python 3.9+ and Node.js 18+
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)
- PostgreSQL database (for production)
- Redis (optional, for session storage)

## Deployment Options

### Option 1: Traditional Server (VPS/Cloud)

Recommended for most deployments.

### Option 2: Platform as a Service (PaaS)

- Heroku
- Railway
- Render
- Fly.io

### Option 3: Containerized (Docker)

See Docker section below.

## Pre-Deployment Checklist

- [ ] Update `SECRET_KEY` environment variable
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up SSL/HTTPS
- [ ] Configure CORS for production domain
- [ ] Set up environment variables
- [ ] Test production build locally
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy

## Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required
SECRET_KEY=your-secret-key-here-min-32-chars

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost/studyhall

# Notion Integration (optional)
NOTION_API_KEY=your_notion_api_key
NOTION_DATABASE_ID=your_notion_database_id

# Flask
FLASK_ENV=production
FLASK_DEBUG=False

# Server
HOST=0.0.0.0
PORT=5000
```

## Backend Deployment

### 1. Install Dependencies

```bash
# On server
cd /path/to/December-Vue-StudyHall/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn  # Production WSGI server
```

### 2. Database Setup

#### SQLite (MVP - Not Recommended for Production)

```bash
python backend/init_db.py
```

#### PostgreSQL (Recommended)

1. Install PostgreSQL:
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
```

2. Create database:
```sql
CREATE DATABASE studyhall;
CREATE USER studyhall_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE studyhall TO studyhall_user;
```

3. Update `backend/database.py`:
```python
# Change SQLite connection to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://studyhall_user:secure_password@localhost/studyhall")
engine = create_engine(DATABASE_URL)
```

4. Initialize database:
```bash
python backend/init_db.py
```

### 3. Run with Gunicorn

Create `gunicorn_config.py`:

```python
bind = "127.0.0.1:5000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
```

Run:
```bash
gunicorn -c gunicorn_config.py backend.main:app
```

### 4. Systemd Service (Linux)

Create `/etc/systemd/system/studyhall.service`:

```ini
[Unit]
Description=StudyHall Flask Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/December-Vue-StudyHall
Environment="PATH=/path/to/December-Vue-StudyHall/backend/.venv/bin"
Environment="PYTHONPATH=/path/to/December-Vue-StudyHall"
ExecStart=/path/to/December-Vue-StudyHall/backend/.venv/bin/gunicorn -c gunicorn_config.py backend.main:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable studyhall
sudo systemctl start studyhall
sudo systemctl status studyhall
```

## Frontend Deployment

### 1. Build Production Bundle

```bash
cd frontend
npm install
npm run build
```

This creates `frontend/dist/` with optimized static files.

### 2. Serve Static Files

#### Option A: Serve with Flask (Simple)

Update `backend/main.py`:

```python
from flask import send_from_directory
import os

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(f"frontend/dist/{path}"):
        return send_from_directory('frontend/dist', path)
    else:
        return send_from_directory('frontend/dist', 'index.html')
```

#### Option B: Nginx (Recommended)

Install Nginx:
```bash
# Ubuntu/Debian
sudo apt-get install nginx

# macOS
brew install nginx
```

Create `/etc/nginx/sites-available/studyhall`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Frontend static files
    root /path/to/December-Vue-StudyHall/frontend/dist;
    index index.html;

    # Frontend routes
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/studyhall /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## SSL/HTTPS Setup

### Let's Encrypt (Free SSL)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal (already configured)
sudo certbot renew --dry-run
```

## Docker Deployment

### Dockerfile

Create `Dockerfile`:

```dockerfile
# Build stage
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Production stage
FROM python:3.9-slim
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy backend
COPY backend/ ./backend/

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Environment
ENV PYTHONPATH=/app
ENV FLASK_ENV=production

# Expose port
EXPOSE 5000

# Run
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.main:app"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://studyhall:password@db/studyhall
      - NOTION_API_KEY=${NOTION_API_KEY}
      - NOTION_DATABASE_ID=${NOTION_DATABASE_ID}
    depends_on:
      - db
    volumes:
      - ./backend/studyhall.db:/app/backend/studyhall.db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=studyhall
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=studyhall
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Build and run:
```bash
docker-compose up -d
```

## PaaS Deployment

### Heroku

1. Install Heroku CLI
2. Create `Procfile`:
```
web: gunicorn backend.main:app
```

3. Create `runtime.txt`:
```
python-3.9.18
```

4. Deploy:
```bash
heroku create studyhall-app
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=postgresql://...
git push heroku master
```

### Railway

1. Connect GitHub repository
2. Set environment variables in dashboard
3. Railway auto-detects and deploys

### Render

1. Create new Web Service
2. Connect repository
3. Set build command: `cd frontend && npm install && npm run build`
4. Set start command: `gunicorn backend.main:app`
5. Set environment variables

## Session Storage (Production)

### Redis Setup

Install Redis:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis
```

Update `backend/services/session.py` to use Redis:

```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def create_session(student_id: int) -> str:
    token = generate_token()
    redis_client.setex(
        f"session:{token}",
        604800,  # 7 days
        json.dumps({"student_id": student_id})
    )
    return token
```

## Monitoring and Logging

### Application Logging

Update `backend/main.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler(
        'logs/studyhall.log',
        maxBytes=10240000,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Health Check Endpoint

Add to `backend/main.py`:

```python
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    })
```

## Backup Strategy

### Database Backups

#### SQLite
```bash
# Daily backup script
cp backend/studyhall.db backups/studyhall-$(date +%Y%m%d).db
```

#### PostgreSQL
```bash
# Daily backup
pg_dump studyhall > backups/studyhall-$(date +%Y%m%d).sql
```

### Automated Backups

Create cron job:
```bash
0 2 * * * /path/to/backup-script.sh
```

## Security Hardening

1. **Firewall**: Configure UFW or iptables
2. **Fail2Ban**: Protect against brute force
3. **Rate Limiting**: Add Flask-Limiter
4. **Security Headers**: Configure in Nginx
5. **Regular Updates**: Keep system and dependencies updated

## Troubleshooting

### Common Issues

**Issue**: 502 Bad Gateway
- Check Gunicorn is running
- Check Nginx configuration
- Check logs: `sudo journalctl -u studyhall`

**Issue**: Database connection errors
- Verify database is running
- Check connection string
- Verify user permissions

**Issue**: Static files not loading
- Check file permissions
- Verify Nginx root path
- Check build output exists

### Logs

**Application logs**:
```bash
tail -f logs/studyhall.log
```

**System logs**:
```bash
sudo journalctl -u studyhall -f
```

**Nginx logs**:
```bash
sudo tail -f /var/log/nginx/error.log
```

## Post-Deployment

1. Test all functionality
2. Monitor error logs
3. Set up uptime monitoring
4. Configure email alerts
5. Document deployment process
6. Create rollback plan

## Maintenance

### Regular Tasks

- Weekly: Review logs and errors
- Monthly: Update dependencies
- Quarterly: Security audit
- As needed: Database backups verification

### Updates

1. Pull latest code
2. Update dependencies
3. Run migrations (if any)
4. Rebuild frontend
5. Restart services
6. Test functionality

## Scaling

### Horizontal Scaling

1. Multiple Gunicorn workers
2. Load balancer (Nginx or cloud LB)
3. Shared session storage (Redis)
4. Shared database (PostgreSQL)

### Vertical Scaling

1. Increase server resources
2. Optimize database queries
3. Add caching layer
4. Use CDN for static assets

## Support

For deployment issues:
1. Check logs
2. Review this documentation
3. Check application documentation
4. Review error messages carefully
