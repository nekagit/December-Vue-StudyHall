from typing import Optional, Dict, List
import secrets
from datetime import datetime, timedelta
from threading import Lock

# In-memory store for pair programming sessions
# In production, use Redis or database-backed sessions
_sessions: Dict[str, Dict] = {}
_session_lock = Lock()

def create_session(host_user_id: Optional[int] = None, host_username: Optional[str] = None) -> str:
    """Create a new pair programming session and return session ID."""
    session_id = secrets.token_urlsafe(16)
    
    with _session_lock:
        _sessions[session_id] = {
            "host_user_id": host_user_id,
            "host_username": host_username or "Host",
            "participants": [],
            "code": 'print("Hello, StudyHall!")',
            "output": "",
            "messages": [],  # Chat messages
            "cursors": {},  # Cursor positions by socket_id
            "selections": {},  # Code selections by socket_id
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=24)
        }
    
    return session_id

def get_session(session_id: str) -> Optional[Dict]:
    """Get session data."""
    with _session_lock:
        if session_id not in _sessions:
            return None
        
        session = _sessions[session_id]
        if datetime.now() > session["expires_at"]:
            del _sessions[session_id]
            return None
        
        return session.copy()

def update_session_code(session_id: str, code: str):
    """Update the code in a session."""
    with _session_lock:
        if session_id in _sessions:
            _sessions[session_id]["code"] = code

def update_session_output(session_id: str, output: str):
    """Update the output in a session."""
    with _session_lock:
        if session_id in _sessions:
            _sessions[session_id]["output"] = output

def add_participant(session_id: str, user_id: Optional[int], username: str, socket_id: str):
    """Add a participant to a session."""
    with _session_lock:
        if session_id not in _sessions:
            return False
        
        # Check if user is already in session
        for participant in _sessions[session_id]["participants"]:
            if participant.get("socket_id") == socket_id:
                # Update last_seen
                participant["last_seen"] = datetime.now()
                return True
        
        _sessions[session_id]["participants"].append({
            "user_id": user_id,
            "username": username or f"User{len(_sessions[session_id]['participants'])}",
            "socket_id": socket_id,
            "joined_at": datetime.now(),
            "last_seen": datetime.now(),
            "is_typing": False
        })
        return True

def remove_participant(session_id: str, socket_id: str):
    """Remove a participant from a session."""
    with _session_lock:
        if session_id in _sessions:
            _sessions[session_id]["participants"] = [
                p for p in _sessions[session_id]["participants"]
                if p.get("socket_id") != socket_id
            ]
            
            # Clean up empty sessions
            if len(_sessions[session_id]["participants"]) == 0:
                # Keep session for a bit in case host reconnects
                pass

def get_participants(session_id: str) -> List[Dict]:
    """Get list of participants in a session."""
    session = get_session(session_id)
    if not session:
        return []
    return session.get("participants", [])

def delete_session(session_id: str):
    """Delete a session."""
    with _session_lock:
        if session_id in _sessions:
            del _sessions[session_id]

def get_all_sessions() -> Dict[str, Dict]:
    """Get all active sessions (for admin/debugging purposes)."""
    with _session_lock:
        # Filter out expired sessions
        active_sessions = {}
        now = datetime.now()
        for session_id, session in _sessions.items():
            if session["expires_at"] > now:
                active_sessions[session_id] = session.copy()
        return active_sessions

def extend_session(session_id: str, hours: int = 24):
    """Extend session expiration time."""
    with _session_lock:
        if session_id in _sessions:
            _sessions[session_id]["expires_at"] = datetime.now() + timedelta(hours=hours)
            return True
        return False

def add_message(session_id: str, username: str, message: str, socket_id: str):
    """Add a chat message to a session."""
    with _session_lock:
        if session_id not in _sessions:
            return False
        
        _sessions[session_id]["messages"].append({
            "username": username,
            "message": message,
            "socket_id": socket_id,
            "timestamp": datetime.now()
        })
        
        # Keep only last 100 messages
        if len(_sessions[session_id]["messages"]) > 100:
            _sessions[session_id]["messages"] = _sessions[session_id]["messages"][-100:]
        
        return True

def update_cursor(session_id: str, socket_id: str, position: Dict):
    """Update cursor position for a participant."""
    with _session_lock:
        if session_id in _sessions:
            _sessions[session_id]["cursors"][socket_id] = {
                **position,
                "updated_at": datetime.now()
            }

def update_selection(session_id: str, socket_id: str, selection: Dict):
    """Update code selection for a participant."""
    with _session_lock:
        if session_id in _sessions:
            if selection:
                _sessions[session_id]["selections"][socket_id] = {
                    **selection,
                    "updated_at": datetime.now()
                }
            else:
                # Remove selection if empty
                _sessions[session_id]["selections"].pop(socket_id, None)

def set_typing(session_id: str, socket_id: str, is_typing: bool):
    """Set typing status for a participant."""
    with _session_lock:
        if session_id in _sessions:
            for participant in _sessions[session_id]["participants"]:
                if participant.get("socket_id") == socket_id:
                    participant["is_typing"] = is_typing
                    participant["last_seen"] = datetime.now()
                    break



