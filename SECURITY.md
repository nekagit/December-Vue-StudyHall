# Security Documentation

Security considerations and best practices for the StudyHall Platform.

## Security Overview

This document outlines security measures, vulnerabilities, and recommendations for the StudyHall Platform. The MVP implementation prioritizes functionality, but production deployments should implement all security best practices.

## Current Security Measures

### Authentication

- **Session-based**: HTTP-only cookies prevent XSS attacks
- **Password Hashing**: SHA-256 (should upgrade to bcrypt)
- **Session Expiration**: 7-day session lifetime
- **Route Protection**: Authentication guards on protected routes

### Data Protection

- **SQL Injection**: Protected by SQLAlchemy ORM
- **XSS Protection**: Vue.js automatically escapes content
- **CORS**: Configured for specific origins
- **Input Validation**: Basic validation in place

## Security Vulnerabilities (MVP)

### Critical Issues

1. **Password Hashing**
   - **Current**: SHA-256 (vulnerable to rainbow tables)
   - **Risk**: High
   - **Fix**: Use bcrypt with salt rounds (see below)

2. **Session Storage**
   - **Current**: In-memory (lost on restart)
   - **Risk**: Medium
   - **Fix**: Use Redis or database-backed sessions

3. **Secret Key**
   - **Current**: Default dev key in code
   - **Risk**: High
   - **Fix**: Use environment variable

### Medium Priority

4. **Rate Limiting**
   - **Current**: None
   - **Risk**: Medium
   - **Fix**: Implement Flask-Limiter

5. **HTTPS**
   - **Current**: HTTP in development
   - **Risk**: Medium
   - **Fix**: Enforce HTTPS in production

6. **Input Validation**
   - **Current**: Basic validation
   - **Risk**: Medium
   - **Fix**: Comprehensive validation library

## Security Best Practices

### Password Security

#### Current Implementation (MVP)

```python
# backend/services/auth.py
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
```

**Issues:**
- No salt
- Fast hashing (vulnerable to brute force)
- No password strength requirements

#### Production Implementation

```python
import bcrypt

def hash_password(password: str) -> str:
    """Hash password using bcrypt with salt."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against bcrypt hash."""
    return bcrypt.checkpw(password.encode(), password_hash.encode())
```

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

### Session Security

#### Current Implementation (MVP)

```python
# In-memory session storage
sessions = {}
```

**Issues:**
- Lost on server restart
- Not scalable across multiple servers
- No expiration cleanup

#### Production Implementation

**Option 1: Redis**
```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def create_session(student_id: int) -> str:
    token = generate_secure_token()
    redis_client.setex(
        f"session:{token}",
        604800,  # 7 days
        json.dumps({"student_id": student_id})
    )
    return token
```

**Option 2: Database-backed**
```python
class Session(Base):
    __tablename__ = "sessions"
    
    token = Column(String, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    expires_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
```

### Environment Variables

#### Never Commit Secrets

**Bad:**
```python
SECRET_KEY = "hardcoded-secret-key"
```

**Good:**
```python
import os
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
```

#### Required Environment Variables

```bash
# Production
SECRET_KEY=your-random-32-character-secret-key
DATABASE_URL=postgresql://user:password@localhost/db
NOTION_API_KEY=your-notion-api-key
NOTION_DATABASE_ID=your-database-id

# Optional
REDIS_URL=redis://localhost:6379/0
FLASK_ENV=production
```

### Input Validation

#### Current Implementation

Basic validation exists but should be enhanced:

```python
# Current
email = data.get("email")
password = data.get("password")
```

#### Enhanced Validation

```python
from email_validator import validate_email, EmailNotValidError

def validate_email_address(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validate_password(password: str) -> tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letter"
    # ... more checks
    return True, ""
```

### SQL Injection Prevention

#### Current Protection

SQLAlchemy ORM protects against SQL injection:

```python
# Safe - uses parameterized queries
student = db.query(Student).filter(Student.email == email).first()
```

#### Never Do This

```python
# DANGEROUS - SQL injection vulnerability
query = f"SELECT * FROM students WHERE email = '{email}'"
```

### XSS Prevention

#### Vue.js Automatic Escaping

Vue.js automatically escapes content:

```vue
<!-- Safe - automatically escaped -->
<div>{{ user_input }}</div>
```

#### Dangerous - Raw HTML

```vue
<!-- DANGEROUS - only use with trusted content -->
<div v-html="user_input"></div>
```

**Safe Alternative:**
```vue
<!-- Use markdown parser or sanitizer -->
<div v-html="sanitize(markdown(user_input))"></div>
```

### CORS Configuration

#### Current Configuration

```python
CORS(app, 
     supports_credentials=True, 
     origins=["http://localhost:5173", "http://localhost:5000"],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
```

#### Production Configuration

```python
# Only allow production domain
CORS(app,
     supports_credentials=True,
     origins=["https://yourdomain.com"],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
```

### Rate Limiting

#### Implementation

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

### HTTPS Enforcement

#### Nginx Configuration

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### Security Headers

Add to Flask responses:

```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    return response
```

## Security Checklist

### Pre-Deployment

- [ ] Change default SECRET_KEY
- [ ] Use environment variables for all secrets
- [ ] Implement bcrypt for password hashing
- [ ] Set up Redis or database-backed sessions
- [ ] Configure HTTPS/SSL
- [ ] Set up rate limiting
- [ ] Configure CORS for production domain
- [ ] Add security headers
- [ ] Enable logging and monitoring
- [ ] Set up backup strategy
- [ ] Review and update dependencies
- [ ] Run security audit tools

### Ongoing Maintenance

- [ ] Regularly update dependencies
- [ ] Monitor security advisories
- [ ] Review access logs
- [ ] Audit user permissions
- [ ] Test backup restoration
- [ ] Review error logs for suspicious activity
- [ ] Keep SSL certificates updated
- [ ] Monitor for brute force attempts

## Dependency Security

### Check for Vulnerabilities

**Python:**
```bash
pip install safety
safety check
```

**Node.js:**
```bash
npm audit
npm audit fix
```

### Keep Dependencies Updated

**Python:**
```bash
pip list --outdated
pip install --upgrade package-name
```

**Node.js:**
```bash
npm outdated
npm update
```

## Incident Response

### If Security Breach Occurs

1. **Immediate Actions**:
   - Take affected systems offline
   - Preserve logs and evidence
   - Change all credentials
   - Notify affected users

2. **Investigation**:
   - Review access logs
   - Identify attack vector
   - Assess data exposure
   - Document findings

3. **Remediation**:
   - Patch vulnerabilities
   - Update security measures
   - Restore from backups if needed
   - Monitor for continued attacks

4. **Post-Incident**:
   - Review security measures
   - Update documentation
   - Train team on lessons learned
   - Consider security audit

## Security Testing

### Manual Testing

1. **Authentication**:
   - Test login with invalid credentials
   - Test session expiration
   - Test logout functionality

2. **Authorization**:
   - Test access to protected routes
   - Test access to other users' data
   - Test privilege escalation

3. **Input Validation**:
   - Test SQL injection attempts
   - Test XSS payloads
   - Test file upload (if applicable)

### Automated Testing

**Tools:**
- OWASP ZAP
- Burp Suite
- SQLMap (for SQL injection testing)
- Snyk (dependency scanning)

## Compliance Considerations

### Data Privacy

- **Student Data**: Store securely, limit access
- **Passwords**: Never store in plain text
- **Logs**: Don't log sensitive information
- **Backups**: Encrypt backups

### GDPR (if applicable)

- Right to access
- Right to deletion
- Data portability
- Privacy policy

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/latest/security/)
- [Vue.js Security](https://vuejs.org/guide/best-practices/security.html)
- [Python Security](https://python.readthedocs.io/en/latest/library/security.html)

## Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT** create a public issue
2. Email security concerns privately
3. Provide detailed description
4. Include steps to reproduce
5. Allow time for fix before disclosure

## Conclusion

Security is an ongoing process. Regularly review and update security measures as threats evolve and the application grows.
