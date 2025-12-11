import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock
from backend.services.session import create_session, get_session, delete_session


class TestCreateSession:
    """Test session creation."""
    
    def test_create_session(self):
        """Test creating a new session."""
        student_id = 1
        token = create_session(student_id)
        
        assert token is not None
        assert len(token) > 0
        assert isinstance(token, str)
    
    def test_create_multiple_sessions(self):
        """Test creating multiple sessions for different students."""
        token1 = create_session(1)
        token2 = create_session(2)
        
        assert token1 != token2  # Different tokens for different students
    
    def test_create_session_stores_data(self):
        """Test that session data is stored correctly."""
        from backend.services.session import _sessions
        
        student_id = 5
        token = create_session(student_id)
        
        assert token in _sessions
        assert _sessions[token]["student_id"] == student_id
        assert "created_at" in _sessions[token]
        assert "expires_at" in _sessions[token]
        assert isinstance(_sessions[token]["created_at"], datetime)
        assert isinstance(_sessions[token]["expires_at"], datetime)


class TestGetSession:
    """Test getting session data."""
    
    def test_get_valid_session(self):
        """Test getting a valid session."""
        student_id = 10
        token = create_session(student_id)
        
        request = Mock()
        request.cookies = {"session_token": token}
        
        session_data = get_session(request)
        
        assert session_data is not None
        assert session_data["student_id"] == student_id
        assert "created_at" in session_data
        assert "expires_at" in session_data
    
    def test_get_invalid_token(self):
        """Test getting session with invalid token."""
        request = Mock()
        request.cookies = {"session_token": "invalid_token"}
        
        session_data = get_session(request)
        
        assert session_data is None
    
    def test_get_missing_token(self):
        """Test getting session without token."""
        request = Mock()
        request.cookies = {}
        
        session_data = get_session(request)
        
        assert session_data is None
    
    def test_get_expired_session(self):
        """Test getting an expired session."""
        from backend.services.session import _sessions
        
        student_id = 20
        token = create_session(student_id)
        
        # Manually expire the session
        _sessions[token]["expires_at"] = datetime.now() - timedelta(days=1)
        
        request = Mock()
        request.cookies = {"session_token": token}
        
        session_data = get_session(request)
        
        assert session_data is None
        assert token not in _sessions  # Should be deleted
    
    def test_get_session_expires_in_7_days(self):
        """Test that sessions expire in 7 days."""
        student_id = 30
        token = create_session(student_id)
        
        request = Mock()
        request.cookies = {"session_token": token}
        
        session_data = get_session(request)
        
        assert session_data is not None
        expires_at = session_data["expires_at"]
        created_at = session_data["created_at"]
        
        # Check that expiration is approximately 7 days from creation
        time_diff = expires_at - created_at
        assert abs(time_diff.total_seconds() - 7 * 24 * 60 * 60) < 60  # Within 1 minute


class TestDeleteSession:
    """Test session deletion."""
    
    def test_delete_existing_session(self):
        """Test deleting an existing session."""
        from backend.services.session import _sessions
        
        student_id = 40
        token = create_session(student_id)
        
        assert token in _sessions
        
        delete_session(token)
        
        assert token not in _sessions
    
    def test_delete_nonexistent_session(self):
        """Test deleting a non-existent session."""
        from backend.services.session import _sessions
        
        # Should not raise an error
        delete_session("nonexistent_token")
        
        # Verify it's still not in sessions
        assert "nonexistent_token" not in _sessions
    
    def test_delete_session_multiple_times(self):
        """Test deleting the same session multiple times."""
        from backend.services.session import _sessions
        
        token = create_session(50)
        
        delete_session(token)
        delete_session(token)  # Should not raise error
        
        assert token not in _sessions


class TestSessionIsolation:
    """Test that sessions are isolated."""
    
    def test_multiple_sessions_independent(self):
        """Test that multiple sessions are independent."""
        from backend.services.session import _sessions
        
        token1 = create_session(1)
        token2 = create_session(2)
        
        assert token1 in _sessions
        assert token2 in _sessions
        assert _sessions[token1]["student_id"] == 1
        assert _sessions[token2]["student_id"] == 2
        
        delete_session(token1)
        
        assert token1 not in _sessions
        assert token2 in _sessions  # Other session still exists




