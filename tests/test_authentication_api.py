import pytest
from backend.services.authentication_service import AuthenticationService

@pytest.fixture
def auth_service():
    return AuthenticationService()

def test_login_success(auth_service):
    
    username = "admin"
    password = "admin123"

    result = auth_service.login(username, password)
    assert result is True

def test_login_failure_wrong_password(auth_service):
    username = "admin"
    password = "wrongpassword"

    result = auth_service.login(username, password)
    assert result is False

def test_login_failure_unknown_user(auth_service):
    username = "nonexistentuser"
    password = "any"

    result = auth_service.login(username, password)
    assert result is False
