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
    """Test session creation."""
    
    def test_create_session(self):
        """Test creating a new session."""
        # Clear sessions before test
        _sessions.clear()
        
        student_id = 1
        token = create_session(student_id)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
        assert token in _sessions
        
        session_data = _sessions[token]
        assert session_data['student_id'] == student_id
        assert 'created_at' in session_data
        assert 'expires_at' in session_data
        assert isinstance(session_data['created_at'], datetime)
        assert isinstance(session_data['expires_at'], datetime)
    
    def test_create_session_multiple(self):
        """Test creating multiple sessions."""
        _sessions.clear()
        
        token1 = create_session(1)
        token2 = create_session(2)
        token3 = create_session(1)  # Same student, different session
        
        assert token1 != token2
        assert token1 != token3
        assert token2 != token3
        assert len(_sessions) == 3
    
    def test_create_session_expires_at(self):
        """Test that session expires_at is set correctly."""
        _sessions.clear()
        
        token = create_session(1)
        session_data = _sessions[token]
        
        # Expires at should be approximately 7 days from now
        expected_expires = datetime.now() + timedelta(days=7)
        time_diff = abs((expected_expires - session_data['expires_at']).total_seconds())
        
        # Allow 1 second tolerance
        assert time_diff < 1


class TestGetSession:
    """Test getting session data."""
    
    def test_get_session_valid(self):
        """Test getting valid session."""
        _sessions.clear()
        
        token = create_session(1)
        
        # Create mock request with cookie
        request = Mock()
        request.cookies = {'session_token': token}
        
        session_data = get_session(request)
        
        assert session_data is not None
        assert session_data['student_id'] == 1
        assert 'created_at' in session_data
        assert 'expires_at' in session_data
    
    def test_get_session_invalid_token(self):
        """Test getting session with invalid token."""
        _sessions.clear()
        
        request = Mock()
        request.cookies = {'session_token': 'invalid_token'}
        
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
        """Test getting expired session."""
        _sessions.clear()
        
        token = create_session(1)
        # Manually expire the session
        _sessions[token]['expires_at'] = datetime.now() - timedelta(days=1)
        
        request = Mock()
        request.cookies = {'session_token': token}
        
        session_data = get_session(request)
        
        assert session_data is None
        # Session should be deleted
        assert token not in _sessions
    
    def test_get_session_no_cookies_attribute(self):
        """Test getting session when request has no cookies attribute."""
        _sessions.clear()
        
        request = Mock()
        del request.cookies  # Remove cookies attribute
        
        session_data = get_session(request)
        
        assert session_data is None


class TestDeleteSession:
    """Test session deletion."""
    
    def test_delete_session_exists(self):
        """Test deleting existing session."""
        _sessions.clear()
        
        token = create_session(1)
        assert token in _sessions
        
        delete_session(token)
        
        assert token not in _sessions
    
    def test_delete_session_not_exists(self):
        """Test deleting non-existent session."""
        _sessions.clear()
        
        # Should not raise an error
        delete_session('nonexistent_token')
        
        assert len(_sessions) == 0
    
    def test_delete_session_multiple(self):
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


class TestSessionIntegration:
    """Integration tests for session management."""
    
    def test_session_lifecycle(self):
        """Test complete session lifecycle."""
        _sessions.clear()
        
        # Create session
        token = create_session(1)
        assert token in _sessions
        
        # Get session
        request = Mock()
        request.cookies = {'session_token': token}
        session_data = get_session(request)
        assert session_data is not None
        assert session_data['student_id'] == 1
        
        # Delete session
        delete_session(token)
        assert token not in _sessions
        
        # Try to get deleted session
        session_data = get_session(request)
        assert session_data is None
    
    def test_session_isolation(self):
        """Test that sessions are isolated per student."""
        _sessions.clear()
        
        token1 = create_session(1)
        token2 = create_session(2)
        
        request1 = Mock()
        request1.cookies = {'session_token': token1}
        
        request2 = Mock()
        request2.cookies = {'session_token': token2}
        
        session1 = get_session(request1)
        session2 = get_session(request2)
        
        assert session1['student_id'] == 1
        assert session2['student_id'] == 2
    
    def test_session_token_uniqueness(self):
        """Test that session tokens are unique."""
        _sessions.clear()
        
        tokens = [create_session(1) for _ in range(100)]
        
        # All tokens should be unique
        assert len(set(tokens)) == 100
        assert len(_sessions) == 100
