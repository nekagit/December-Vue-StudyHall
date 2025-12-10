import pytest
from datetime import datetime, timedelta
from backend.services.session import create_session, get_session, delete_session
from unittest.mock import Mock

def test_create_session():
    """Test session creation."""
    student_id = 1
    token = create_session(student_id)
    
    assert token is not None
    assert len(token) > 0

def test_get_session_valid():
    """Test getting a valid session."""
    student_id = 1
    token = create_session(student_id)
    
    request = Mock()
    request.cookies = {"session_token": token}
    
    session_data = get_session(request)
    assert session_data is not None
    assert session_data["student_id"] == student_id
    assert "created_at" in session_data
    assert "expires_at" in session_data

def test_get_session_invalid_token():
    """Test getting session with invalid token."""
    request = Mock()
    request.cookies = {"session_token": "invalid_token"}
    
    session_data = get_session(request)
    assert session_data is None

def test_get_session_no_token():
    """Test getting session with no token."""
    request = Mock()
    request.cookies = {}
    
    session_data = get_session(request)
    assert session_data is None

def test_delete_session():
    """Test session deletion."""
    student_id = 1
    token = create_session(student_id)
    
    request = Mock()
    request.cookies = {"session_token": token}
    
    # Verify session exists
    assert get_session(request) is not None
    
    # Delete session
    delete_session(token)
    
    # Verify session is gone
    assert get_session(request) is None
