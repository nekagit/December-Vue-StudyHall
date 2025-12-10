from typing import Optional
import secrets
from datetime import datetime, timedelta

# Simple in-memory session store for MVP
# In production, use Redis or database-backed sessions
_sessions: dict[str, dict] = {}

def create_session(student_id: int) -> str:
    """Create a new session and return session token."""
    token = secrets.token_urlsafe(32)
    _sessions[token] = {
        "student_id": student_id,
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(days=7)
    }
    return token

def get_session(request) -> Optional[dict]:
    """Get session from request cookies."""
    token = request.cookies.get("session_token") if hasattr(request, 'cookies') else None
    if not token or token not in _sessions:
        return None
    
    session_data = _sessions[token]
    if datetime.now() > session_data["expires_at"]:
        del _sessions[token]
        return None
    
    return session_data

def delete_session(token: str):
    """Delete a session."""
    if token in _sessions:
        del _sessions[token]

