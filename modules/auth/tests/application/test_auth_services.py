import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException

from modules.auth.application.auth_services import AuthServices, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context
from modules.auth.domain.user import User, UserRole
from modules.auth.domain.user_repository_interface import UserRepositoryInterface

# Mock del UserRepositoryInterface
@pytest.fixture
def mock_user_repo():
    return Mock(spec=UserRepositoryInterface)

@pytest.fixture
def auth_services(mock_user_repo):
    return AuthServices(user_repo=mock_user_repo)

@pytest.fixture
def sample_user():
    return User(
        uuid="a1b2c3d4-e5f6-7890-1234-567890abcdef",
        name="Test User",
        email="test@example.com",
        hashed_password=pwd_context.hash("password123"),
        role=UserRole.CLIENT
    )

@pytest.fixture
def admin_user():
    return User(
        uuid="b1c2d3e4-f5a6-7890-1234-567890abcdef",
        name="Admin User",
        email="admin@example.com",
        hashed_password=pwd_context.hash("adminpass"),
        role=UserRole.ADMIN
    )


# Tests para authenticate_user
def test_authenticate_user_success(auth_services, mock_user_repo, sample_user):
    mock_user_repo.get_by_email.return_value = sample_user
    authenticated_user = auth_services.authenticate_user("test@example.com", "password123")
    assert authenticated_user == sample_user
    mock_user_repo.get_by_email.assert_called_once_with("test@example.com")

def test_authenticate_user_wrong_password(auth_services, mock_user_repo, sample_user):
    mock_user_repo.get_by_email.return_value = sample_user
    authenticated_user = auth_services.authenticate_user("test@example.com", "wrongpassword")
    assert authenticated_user is None
    mock_user_repo.get_by_email.assert_called_once_with("test@example.com")

def test_authenticate_user_not_found(auth_services, mock_user_repo):
    mock_user_repo.get_by_email.return_value = None
    authenticated_user = auth_services.authenticate_user("nonexistent@example.com", "password123")
    assert authenticated_user is None
    mock_user_repo.get_by_email.assert_called_once_with("nonexistent@example.com")

# Tests para create_access_token
def test_create_access_token_default_expiration(auth_services, sample_user):
    data = {"sub": str(sample_user.uuid)}
    scopes = ["client:read"]
    token = auth_services.create_access_token(data, scopes)
    assert isinstance(token, str)

    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_payload["sub"] == str(sample_user.uuid)
    assert "scopes" in decoded_payload
    assert "client:read" in decoded_payload["scopes"]
    assert "exp" in decoded_payload
    # Check expiration is roughly within expected range
    expected_expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    assert decoded_payload["exp"] <= int(expected_expire_time.timestamp()) + 5 # Allow small buffer

def test_create_access_token_custom_expiration(auth_services, sample_user):
    data = {"sub": str(sample_user.uuid)}
    scopes = ["client:write"]
    custom_delta = timedelta(minutes=5)
    token = auth_services.create_access_token(data, scopes, expires_delta=custom_delta)
    assert isinstance(token, str)

    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_payload["sub"] == str(sample_user.uuid)
    assert "scopes" in decoded_payload
    assert "client:write" in decoded_payload["scopes"]
    assert "exp" in decoded_payload
    expected_expire_time = datetime.utcnow() + custom_delta
    assert decoded_payload["exp"] <= int(expected_expire_time.timestamp()) + 5 # Allow small buffer

# Tests para get_current_user
def test_get_current_user_success(auth_services, mock_user_repo, sample_user):
    mock_user_repo.get_by_id.return_value = sample_user
    token_data = {"sub": str(sample_user.uuid), "scopes": ["client:read", "client:write"]}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    current_user = auth_services.get_current_user(token, ["client:read"])
    assert current_user == sample_user
    mock_user_repo.get_by_id.assert_called_once_with(str(sample_user.uuid))

def test_get_current_user_expired_token(auth_services):
    expired_token_data = {"sub": "some_uuid", "exp": datetime.utcnow() - timedelta(minutes=1), "scopes": ["client:read"]}
    expired_token = jwt.encode(expired_token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as exc_info:
        auth_services.get_current_user(expired_token, ["client:read"])
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Expired token"

def test_get_current_user_invalid_token(auth_services):
    with pytest.raises(HTTPException) as exc_info:
        auth_services.get_current_user("invalid.jwt.token", ["client:read"])
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token error"

def test_get_current_user_insufficient_scopes(auth_services, mock_user_repo, sample_user):
    mock_user_repo.get_by_id.return_value = sample_user
    token_data = {"sub": str(sample_user.uuid), "scopes": ["client:read"]}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as exc_info:
        auth_services.get_current_user(token, ["admin:all"])
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You dont have access to this endpoint"

def test_get_current_user_user_not_found_from_token(auth_services, mock_user_repo):
    mock_user_repo.get_by_id.return_value = None
    token_data = {"sub": "nonexistent_uuid", "scopes": ["client:read"]}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    current_user = auth_services.get_current_user(token, ["client:read"])
    assert current_user is None
    mock_user_repo.get_by_id.assert_called_once_with("nonexistent_uuid")
