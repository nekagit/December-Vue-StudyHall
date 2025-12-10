# Troubleshooting Guide

Common issues and solutions for the StudyHall Platform.

## Table of Contents

- [Setup Issues](#setup-issues)
- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [Database Issues](#database-issues)
- [Authentication Issues](#authentication-issues)
- [API Issues](#api-issues)
- [Build Issues](#build-issues)
- [Deployment Issues](#deployment-issues)

## Setup Issues

### Python Virtual Environment Not Activating

**Symptoms**: `source .venv/bin/activate` doesn't work

**Solutions**:
```bash
# Check Python version
python3 --version  # Should be 3.9+

# Recreate virtual environment
rm -rf backend/.venv
python3 -m venv backend/.venv
source backend/.venv/bin/activate

# On Windows
backend\.venv\Scripts\activate
```

### Dependencies Installation Fails

**Symptoms**: `pip install -r requirements.txt` fails

**Solutions**:
```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Install individually to identify problem package
pip install flask
pip install flask-cors
# etc.
```

### Node Modules Installation Fails

**Symptoms**: `npm install` fails or hangs

**Solutions**:
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Use different registry (if needed)
npm install --registry https://registry.npmjs.org/
```

## Backend Issues

### Flask Server Won't Start

**Symptoms**: `python backend/main.py` fails

**Solutions**:
```bash
# Check Python path
export PYTHONPATH=$(pwd)

# Check for syntax errors
python -m py_compile backend/main.py

# Check imports
python -c "from backend.main import app"

# Check port availability
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows
```

### Import Errors

**Symptoms**: `ModuleNotFoundError` or `ImportError`

**Solutions**:
```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=$(pwd)

# Verify virtual environment is activated
which python  # Should show .venv path

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### Database Connection Errors

**Symptoms**: `OperationalError` or database locked

**Solutions**:
```bash
# Check database file exists
ls -la backend/studyhall.db

# Check file permissions
chmod 644 backend/studyhall.db

# Close any open database connections
# Restart Flask server

# If locked, delete and recreate
rm backend/studyhall.db
python backend/init_db.py
```

### CORS Errors

**Symptoms**: Browser console shows CORS errors

**Solutions**:
1. Check `backend/main.py` CORS configuration:
```python
CORS(app, 
     supports_credentials=True, 
     origins=["http://localhost:5173"])
```

2. Verify frontend URL matches CORS origins
3. Check browser console for exact error
4. Ensure `credentials: 'include'` in fetch calls

## Frontend Issues

### Dev Server Won't Start

**Symptoms**: `npm run dev` fails

**Solutions**:
```bash
# Check Node.js version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules .vite
npm install

# Check port availability
lsof -i :5173  # macOS/Linux
```

### TypeScript Errors

**Symptoms**: TypeScript compilation errors

**Solutions**:
```bash
# Check TypeScript version
npx tsc --version

# Run type check
npm run build  # Shows TypeScript errors

# Fix common issues:
# - Add type annotations
# - Fix import paths
# - Update type definitions
```

### Styles Not Loading

**Symptoms**: TailwindCSS styles not applied

**Solutions**:
1. Check `src/style.scss` imports TailwindCSS:
```scss
@import "tailwindcss";
```

2. Verify `vite.config.ts` includes TailwindCSS plugin
3. Restart dev server
4. Clear browser cache

### Hot Module Replacement Not Working

**Symptoms**: Changes don't reflect without refresh

**Solutions**:
```bash
# Restart dev server
# Stop server (Ctrl+C) and restart

# Clear Vite cache
rm -rf .vite
npm run dev

# Check file watchers (Linux)
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## Database Issues

### Database File Not Found

**Symptoms**: `OperationalError: no such table`

**Solutions**:
```bash
# Initialize database
python backend/init_db.py

# Verify tables exist
sqlite3 backend/studyhall.db ".tables"
```

### Migration Issues

**Symptoms**: Schema changes not reflected

**Solutions**:
```bash
# For MVP: Delete and recreate
rm backend/studyhall.db
python backend/init_db.py

# For production: Use Alembic migrations
alembic upgrade head
```

### Data Loss

**Symptoms**: Data disappears after restart

**Solutions**:
1. Check if using in-memory database (shouldn't be)
2. Verify database file path
3. Check file permissions
4. Restore from backup if available

## Authentication Issues

### Login Not Working

**Symptoms**: Login fails or redirects immediately

**Solutions**:
1. Check credentials:
   - Default: `student@studyhall.com` / `password123`
2. Verify session cookie is set:
   - Check browser DevTools > Application > Cookies
3. Check backend logs for errors
4. Verify CORS and credentials:
```typescript
fetch('/api/auth/login', {
  credentials: 'include'  // Important!
})
```

### Session Expires Immediately

**Symptoms**: Logged out right after login

**Solutions**:
1. Check cookie settings in `backend/main.py`:
```python
response.set_cookie("session_token", token, httponly=True, max_age=604800)
```

2. Verify session storage is working
3. Check browser cookie settings
4. Clear browser cookies and try again

### Protected Routes Not Working

**Symptoms**: Can access protected routes without login

**Solutions**:
1. Check router guard in `src/main.ts`
2. Verify `requiresAuth` meta on routes
3. Check cookie reading logic
4. Test authentication endpoint directly

## API Issues

### 404 Not Found

**Symptoms**: API endpoints return 404

**Solutions**:
1. Verify Flask server is running
2. Check endpoint URL matches backend route
3. Verify proxy configuration in `vite.config.ts`:
```typescript
proxy: {
  '/api': 'http://localhost:5000'
}
```

### 401 Unauthorized

**Symptoms**: API returns 401 even when logged in

**Solutions**:
1. Check session token in cookies
2. Verify `credentials: 'include'` in fetch
3. Check backend session validation
4. Try logging out and back in

### 500 Internal Server Error

**Symptoms**: Server errors on API calls

**Solutions**:
1. Check backend logs for error details
2. Verify database connection
3. Check environment variables
4. Review error handling in endpoint

## Build Issues

### Frontend Build Fails

**Symptoms**: `npm run build` errors

**Solutions**:
```bash
# Check TypeScript errors
npm run build  # Shows errors

# Fix type errors
# Update dependencies
npm update

# Clear build cache
rm -rf dist .vite
npm run build
```

### Production Build Not Working

**Symptoms**: Built app doesn't work when served

**Solutions**:
1. Check base path in `vite.config.ts`
2. Verify API proxy (not used in production)
3. Update API URLs to production domain
4. Check static file serving configuration

## Deployment Issues

### Application Won't Start

**Symptoms**: Production app doesn't start

**Solutions**:
1. Check environment variables:
```bash
echo $SECRET_KEY
echo $DATABASE_URL
```

2. Verify Gunicorn is installed:
```bash
pip install gunicorn
```

3. Check logs:
```bash
sudo journalctl -u studyhall -f
```

4. Test locally with production settings

### Database Connection in Production

**Symptoms**: Can't connect to production database

**Solutions**:
1. Verify `DATABASE_URL` environment variable
2. Check database server is running
3. Verify network connectivity
4. Check firewall rules
5. Verify credentials

### Static Files Not Loading

**Symptoms**: CSS/JS files return 404

**Solutions**:
1. Verify build output exists: `ls -la frontend/dist/`
2. Check Nginx/Flask static file configuration
3. Verify file permissions
4. Check base path configuration

## Performance Issues

### Slow API Responses

**Symptoms**: API calls are slow

**Solutions**:
1. Check database queries (add indexes)
2. Review N+1 query problems
3. Add caching layer
4. Check server resources
5. Review slow query logs

### Frontend Slow to Load

**Symptoms**: Page loads slowly

**Solutions**:
1. Check bundle size: `npm run build` shows sizes
2. Enable code splitting
3. Optimize images
4. Use lazy loading for routes
5. Check network tab in DevTools

## Debugging Tips

### Enable Debug Logging

**Backend**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Frontend**:
```typescript
console.log('Debug:', data)
console.error('Error:', error)
```

### Check Logs

**Backend logs**:
```bash
# If using systemd
sudo journalctl -u studyhall -f

# If running directly
python backend/main.py  # Errors print to console
```

**Frontend logs**:
- Browser DevTools > Console
- Network tab for API calls

### Common Debugging Commands

```bash
# Check what's running on ports
lsof -i :5000  # Backend
lsof -i :5173  # Frontend

# Check database
sqlite3 backend/studyhall.db ".tables"
sqlite3 backend/studyhall.db "SELECT * FROM students;"

# Check Python environment
which python
pip list

# Check Node environment
which node
npm list
```

## Getting Help

If issues persist:

1. **Check Documentation**:
   - `README.md` - Setup instructions
   - `DEVELOPMENT.md` - Development guide
   - `API.md` - API reference

2. **Review Logs**: Check error messages carefully

3. **Search Issues**: Check GitHub issues (if public)

4. **Minimal Reproduction**: Create minimal test case

5. **Environment Info**: Include:
   - OS version
   - Python version
   - Node.js version
   - Error messages
   - Steps to reproduce

## Prevention

To avoid common issues:

1. **Follow Setup Guide**: Use `DEVELOPMENT.md`
2. **Keep Dependencies Updated**: Regular `npm update` and `pip install --upgrade`
3. **Use Version Control**: Commit working state
4. **Test Locally**: Before deploying
5. **Read Error Messages**: They often contain solutions
6. **Check Logs**: First step in debugging
