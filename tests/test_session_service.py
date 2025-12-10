import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock
from backend.services.session import (
    create_session,
    get_session,
    delete_session,
    _sessions
)


class TestCreateSession:
    """Tests for session creation."""
    
    def test_create_session(self):
        """Test creating a session."""
        # Clear sessions before test
        _sessions.clear()
        
        student_id = 1
        token = create_session(student_id)
        
        assert token is not None
        assert len(token) > 0
        assert token in _sessions
        assert _sessions[token]["student_id"] == student_id
        assert "created_at" in _sessions[token]
        assert "expires_at" in _sessions[token]
    
    def test_create_session_unique_tokens(self):
        """Test that each session gets a unique token."""
        _sessions.clear()
        
        token1 = create_session(1)
        token2 = create_session(2)
        
        assert token1 != token2
        assert len(_sessions) == 2
    
    def test_create_session_expires_in_7_days(self):
        """Test that session expires in 7 days."""
        _sessions.clear()
        
        student_id = 1
        token = create_session(student_id)
        session_data = _sessions[token]
        
        expected_expires = session_data["created_at"] + timedelta(days=7)
        assert abs((session_data["expires_at"] - expected_expires).total_seconds()) < 1


class TestGetSession:
    """Tests for getting session data."""
    
    def test_get_session_valid(self):
        """Test getting a valid session."""
        _sessions.clear()
        
        student_id = 1
        token = create_session(student_id)
        
        # Mock request object
        request = Mock()
        request.cookies = {"session_token": token}
        
        session_data = get_session(request)
        
        assert session_data is not None
        assert session_data["student_id"] == student_id
    
    def test_get_session_invalid_token(self):
        """Test getting session with invalid token."""
        _sessions.clear()
        
        request = Mock()
        request.cookies = {"session_token": "invalid-token"}
        
        session_data = get_session(request)
        
        assert session_data is None
    
    def test_get_session_no_cookie(self):
        """Test getting session when no cookie is present."""
        _sessions.clear()
        
        request = Mock()
        request.cookies = {}
        
        session_data = get_session(request)
        
        assert session_data is None
    
    def test_get_session_expired(self):
        """Test getting an expired session."""
        _sessions.clear()
        
        student_id = 1
        token = create_session(student_id)
        
        # Manually expire the session
        _sessions[token]["expires_at"] = datetime.now() - timedelta(days=1)
        
        request = Mock()
        request.cookies = {"session_token": token}
        
        session_data = get_session(request)
        
        assert session_data is None
        assert token not in _sessions  # Should be deleted
    
    def test_get_session_no_cookies_attribute(self):
        """Test get_session when request has no cookies attribute."""
        _sessions.clear()
        
        request = Mock()
        del request.cookies  # Remove cookies attribute
        
        session_data = get_session(request)
        
        assert session_data is None


class TestDeleteSession:
    """Tests for deleting sessions."""
    
    def test_delete_session_exists(self):
        """Test deleting an existing session."""
        _sessions.clear()
        
        student_id = 1
        token = create_session(student_id)
        
        assert token in _sessions
        
        delete_session(token)
        
        assert token not in _sessions
    
    def test_delete_session_not_exists(self):
        """Test deleting a non-existent session."""
        _sessions.clear()
        
        # Should not raise an error
        delete_session("non-existent-token")
        
        assert len(_sessions) == 0
    
    def test_delete_session_multiple_sessions(self):
        """Test deleting one session doesn't affect others."""
        _sessions.clear()
        
        token1 = create_session(1)
        token2 = create_session(2)
        token3 = create_session(3)
        
        assert len(_sessions) == 3
        
        delete_session(token2)
        
        assert token1 in _sessions
        assert token2 not in _sessions
        assert token3 in _sessions
        assert len(_sessions) == 2
