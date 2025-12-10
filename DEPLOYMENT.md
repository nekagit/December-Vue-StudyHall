# Deployment Guide

This guide covers deploying the StudyHall Platform to production environments.

## Overview

The StudyHall Platform consists of:
- **Frontend**: Vue.js SPA (static files)
- **Backend**: Flask REST API (Python application)
- **Database**: SQLite (MVP) or PostgreSQL (recommended for production)

## Pre-Deployment Checklist

- [ ] Update `SECRET_KEY` environment variable
- [ ] Change default student password
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure CORS for production domain
- [ ] Set up session storage (Redis recommended)
- [ ] Configure logging
- [ ] Set up monitoring/alerting
- [ ] Review security settings
- [ ] Test production build locally

## Production Architecture

### Recommended Setup

```
┌─────────────────┐
│   Nginx         │  Reverse Proxy + Static Files
│   (Port 80/443) │
└────────┬────────┘
         │
         ├──► /api/* → Gunicorn (Flask API)
         │
         └──► /* → Static Files (Vite build)
```

### Components

1. **Nginx**: Reverse proxy and static file server
2. **Gunicorn**: WSGI HTTP Server for Flask
3. **PostgreSQL**: Production database (or keep SQLite for small deployments)
4. **Redis**: Session storage (optional but recommended)
5. **SSL/TLS**: HTTPS certificates (Let's Encrypt)

## Deployment Options

### Option 1: Single Server (Simple)

Good for small deployments (< 100 users).

**Requirements:**
- Linux server (Ubuntu 20.04+ recommended)
- Python 3.9+
- Node.js 18+
- Nginx
- PostgreSQL (optional, SQLite works for small scale)

### Option 2: Containerized (Docker)

Good for scalability and consistency.

**Requirements:**
- Docker and Docker Compose
- Or Kubernetes (for advanced setups)

### Option 3: Platform as a Service (PaaS)

Good for quick deployment without server management.

**Options:**
- Heroku
- Railway
- Render
- Fly.io
- DigitalOcean App Platform

## Single Server Deployment

### 1. Server Setup

**Update system:**
```bash
sudo apt update
sudo apt upgrade -y
```

**Install dependencies:**
```bash
# Python
sudo apt install python3 python3-pip python3-venv -y

# Node.js (using NodeSource)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# PostgreSQL (optional)
sudo apt install postgresql postgresql-contrib -y

# Nginx
sudo apt install nginx -y

# Redis (optional, for sessions)
sudo apt install redis-server -y
```

### 2. Application Setup

**Clone repository:**
```bash
cd /var/www
sudo git clone https://github.com/your-org/December-Vue-StudyHall.git studyhall
sudo chown -R $USER:$USER studyhall
cd studyhall
```

**Backend setup:**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn  # Add to requirements.txt for production
cd ..
```

**Frontend build:**
```bash
cd frontend
npm install
npm run build
cd ..
```

**Initialize database:**
```bash
source backend/.venv/bin/activate
python backend/init_db.py
```

### 3. Environment Configuration

**Create `.env` file:**
```bash
cd /var/www/studyhall
nano .env
```

**Contents:**
```bash
# Flask
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=production

# Database (PostgreSQL example)
DATABASE_URL=postgresql://studyhall:password@localhost/studyhall

# Or SQLite (simpler, less scalable)
# DATABASE_URL=sqlite:///studyhall.db

# Notion (optional)
NOTION_API_KEY=secret_...
NOTION_DATABASE_ID=...

# CORS (your domain)
ALLOWED_ORIGINS=https://yourdomain.com
```

**Update `backend/main.py` to use environment variables:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.secret_key = os.getenv("SECRET_KEY")
CORS(app, supports_credentials=True, origins=os.getenv("ALLOWED_ORIGINS", "").split(","))
```

### 4. PostgreSQL Setup (Optional)

**Create database:**
```bash
sudo -u postgres psql

CREATE DATABASE studyhall;
CREATE USER studyhall WITH PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE studyhall TO studyhall;
\q
```

**Update `backend/database.py` to use PostgreSQL:**
```python
import os
from sqlalchemy import create_engine

database_url = os.getenv("DATABASE_URL", "sqlite:///studyhall.db")
engine = create_engine(database_url)
```

### 5. Gunicorn Configuration

**Create `gunicorn_config.py`:**
```python
bind = "127.0.0.1:5000"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
```

**Test Gunicorn:**
```bash
cd /var/www/studyhall
source backend/.venv/bin/activate
gunicorn -c gunicorn_config.py backend.main:app
```

### 6. Systemd Service

**Create `/etc/systemd/system/studyhall.service`:**
```ini
[Unit]
Description=StudyHall Flask API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/studyhall
Environment="PATH=/var/www/studyhall/backend/.venv/bin"
Environment="PYTHONPATH=/var/www/studyhall"
ExecStart=/var/www/studyhall/backend/.venv/bin/gunicorn -c gunicorn_config.py backend.main:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable studyhall
sudo systemctl start studyhall
sudo systemctl status studyhall
```

### 7. Nginx Configuration

**Create `/etc/nginx/sites-available/studyhall`:**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static files (Vite build)
    root /var/www/studyhall/frontend/dist;
    index index.html;

    # API proxy
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Cookie $http_cookie;
    }

    # Frontend SPA (all routes)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache static assets
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/studyhall /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. SSL Certificate (Let's Encrypt)

**Install Certbot:**
```bash
sudo apt install certbot python3-certbot-nginx -y
```

**Obtain certificate:**
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

**Auto-renewal (already configured by certbot):**
```bash
sudo certbot renew --dry-run
```

## Docker Deployment

### Dockerfile (Backend)

**Create `Dockerfile.backend`:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY backend/ ./backend/
COPY database.py ./
COPY models/ ./models/
COPY services/ ./services/

ENV PYTHONPATH=/app
EXPOSE 5000

CMD ["gunicorn", "-c", "gunicorn_config.py", "backend.main:app"]
```

### Dockerfile (Frontend)

**Create `Dockerfile.frontend`:**
```dockerfile
FROM node:18-alpine AS build

WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

### Docker Compose

**Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=postgresql://studyhall:password@db/studyhall
    ports:
      - "5000:5000"
    depends_on:
      - db

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend

  db:
    image: postgres:14
    environment:
      - POSTGRES_DB=studyhall
      - POSTGRES_USER=studyhall
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

**Deploy:**
```bash
docker-compose up -d
```

## PaaS Deployment Examples

### Heroku

**Create `Procfile`:**
```
web: gunicorn -c gunicorn_config.py backend.main:app
```

**Create `runtime.txt`:**
```
python-3.9.18
```

**Deploy:**
```bash
heroku create studyhall-app
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=postgresql://...
git push heroku main
```

### Railway

1. Connect GitHub repository
2. Set environment variables
3. Configure build command: `cd frontend && npm install && npm run build`
4. Configure start command: `gunicorn backend.main:app`
5. Deploy

## Security Hardening

### 1. Environment Variables

- Never commit `.env` files
- Use secure secret management (AWS Secrets Manager, HashiCorp Vault)
- Rotate secrets regularly

### 2. Database Security

- Use strong passwords
- Limit database access to application server only
- Enable SSL for database connections
- Regular backups

### 3. Application Security

- Update dependencies regularly
- Use HTTPS only
- Implement rate limiting
- Add CSRF protection
- Sanitize all inputs
- Use parameterized queries (already using SQLAlchemy)

### 4. Server Security

- Keep system updated
- Configure firewall (UFW)
- Disable root SSH login
- Use SSH keys instead of passwords
- Set up fail2ban

## Monitoring & Logging

### Application Logs

**Gunicorn logging:**
```python
# In gunicorn_config.py
accesslog = "/var/log/studyhall/access.log"
errorlog = "/var/log/studyhall/error.log"
loglevel = "info"
```

### System Logs

```bash
# View application logs
sudo journalctl -u studyhall -f

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Monitoring Tools

- **Uptime monitoring**: UptimeRobot, Pingdom
- **Application monitoring**: Sentry, Rollbar
- **Server monitoring**: Datadog, New Relic, Prometheus

## Backup Strategy

### Database Backups

**PostgreSQL:**
```bash
# Daily backup script
pg_dump -U studyhall studyhall > backup_$(date +%Y%m%d).sql
```

**SQLite:**
```bash
# Simple copy
cp studyhall.db backup_$(date +%Y%m%d).db
```

**Automated backups:**
```bash
# Add to crontab
0 2 * * * /path/to/backup-script.sh
```

### Application Backups

- Backup code repository (Git)
- Backup uploaded files (if any)
- Backup configuration files

## Scaling Considerations

### Horizontal Scaling

- Multiple Gunicorn workers
- Load balancer (Nginx, HAProxy)
- Multiple application servers
- Shared session storage (Redis)
- Shared database (PostgreSQL)

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Add caching layer (Redis)

## Troubleshooting

### Application Not Starting

```bash
# Check service status
sudo systemctl status studyhall

# Check logs
sudo journalctl -u studyhall -n 50

# Test manually
cd /var/www/studyhall
source backend/.venv/bin/activate
gunicorn backend.main:app
```

### Nginx Errors

```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Reload configuration
sudo systemctl reload nginx
```

### Database Connection Issues

```bash
# Test PostgreSQL connection
psql -U studyhall -d studyhall -h localhost

# Check PostgreSQL status
sudo systemctl status postgresql
```

## Maintenance

### Updating Application

```bash
cd /var/www/studyhall
git pull origin main
source backend/.venv/bin/activate
pip install -r backend/requirements.txt
cd frontend
npm install
npm run build
sudo systemctl restart studyhall
```

### Database Migrations

For production, use Alembic for migrations:
```bash
alembic upgrade head
```

## Support

For deployment issues:
- Check logs first
- Review this guide
- Check GitHub Issues
- Contact maintainers

Good luck with your deployment! 🚀
