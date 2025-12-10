import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from backend.services.session import (
    create_session,
    get_session,
    delete_session,
    _sessions
)


class TestSessionService:
    """Test session management service."""
    
    def setup_method(self):
        """Clear sessions before each test."""
        _sessions.clear()
    
    def test_create_session(self):
        """Test creating a new session."""
        student_id = 1
        token = create_session(student_id)
        
        assert token is not None
        assert len(token) > 0
        assert token in _sessions
        
        session_data = _sessions[token]
        assert session_data["student_id"] == student_id
        assert "created_at" in session_data
        assert "expires_at" in session_data
        assert isinstance(session_data["created_at"], datetime)
        assert isinstance(session_data["expires_at"], datetime)
    
    def test_create_session_unique_tokens(self):
        """Test that each session gets a unique token."""
        token1 = create_session(1)
        token2 = create_session(2)
        
        assert token1 != token2
        assert len(_sessions) == 2
    
    def test_get_session_valid(self):
        """Test getting a valid session."""
        student_id = 1
        token = create_session(student_id)
        
        # Create a mock request with the cookie
        mock_request = MagicMock()
        mock_request.cookies = {"session_token": token}
        
        session_data = get_session(mock_request)
        
        assert session_data is not None
        assert session_data["student_id"] == student_id
    
    def test_get_session_invalid_token(self):
        """Test getting session with invalid token."""
        mock_request = MagicMock()
        mock_request.cookies = {"session_token": "invalid_token"}
        
        session_data = get_session(mock_request)
        
        assert session_data is None
    
    def test_get_session_no_cookie(self):
        """Test getting session when no cookie is present."""
        mock_request = MagicMock()
        mock_request.cookies = {}
        
        session_data = get_session(mock_request)
        
        assert session_data is None
    
    def test_get_session_expired(self):
        """Test getting an expired session."""
        student_id = 1
        token = create_session(student_id)
        
        # Manually expire the session
        _sessions[token]["expires_at"] = datetime.now() - timedelta(days=1)
        
        mock_request = MagicMock()
        mock_request.cookies = {"session_token": token}
        
        session_data = get_session(mock_request)
        
        assert session_data is None
        assert token not in _sessions  # Should be cleaned up
    
    def test_delete_session(self):
        """Test deleting a session."""
        student_id = 1
        token = create_session(student_id)
        
        assert token in _sessions
        
        delete_session(token)
        
        assert token not in _sessions
    
    def test_delete_session_nonexistent(self):
        """Test deleting a non-existent session."""
        # Should not raise an error
        delete_session("nonexistent_token")
    
    def test_session_expiration_time(self):
        """Test that sessions expire after 7 days."""
        student_id = 1
        token = create_session(student_id)
        
        session_data = _sessions[token]
        expires_at = session_data["expires_at"]
        created_at = session_data["created_at"]
        
        # Check that expiration is approximately 7 days from creation
        time_diff = expires_at - created_at
        assert time_diff.days == 7
        assert time_diff.total_seconds() > 0
