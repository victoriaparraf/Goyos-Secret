import pytest
from unittest.mock import Mock
from uuid import UUID, uuid4
from fastapi import HTTPException
from passlib.context import CryptContext

from modules.auth.application.user_services import UserServices
from modules.auth.application.dtos.user_modify_dto import UserModifyDto
from modules.auth.application.dtos.user_register_dto import UserRegisterDto
from modules.auth.domain.user import User, UserRole
from modules.auth.domain.user_repository_interface import UserRepositoryInterface

pwd_context = CryptContext(schemes=["bcrypt"])

# Mock del UserRepositoryInterface
@pytest.fixture
def mock_user_repo():
    return Mock(spec=UserRepositoryInterface)

@pytest.fixture
def user_services(mock_user_repo):
    return UserServices(user_repo=mock_user_repo)

@pytest.fixture
def sample_user():
    return User(
        uuid=uuid4(),
        name="Test User",
        email="test@example.com",
        hashed_password=pwd_context.hash("password123"),
        role=UserRole.CLIENT
    )

@pytest.fixture
def admin_user():
    return User(
        uuid=uuid4(),
        name="Admin User",
        email="admin@example.com",
        hashed_password=pwd_context.hash("adminpass"),
        role=UserRole.ADMIN
    )

# Tests para get_user_by_id
def test_get_user_by_id_success(user_services, mock_user_repo, sample_user):
    mock_user_repo.get_by_id.return_value = sample_user
    user = user_services.get_user_by_id(sample_user.uuid)
    assert user == sample_user
    mock_user_repo.get_by_id.assert_called_once_with(sample_user.uuid)

def test_get_user_by_id_not_found(user_services, mock_user_repo):
    mock_user_repo.get_by_id.return_value = None
    user = user_services.get_user_by_id(uuid4())
    assert user is None

# Tests para get_user_by_email
def test_get_user_by_email_success(user_services, mock_user_repo, sample_user):
    mock_user_repo.get_by_email.return_value = sample_user
    user = user_services.get_user_by_email("test@example.com")
    assert user == sample_user
    mock_user_repo.get_by_email.assert_called_once_with("test@example.com")

def test_get_user_by_email_not_found(user_services, mock_user_repo):
    mock_user_repo.get_by_email.return_value = None
    user = user_services.get_user_by_email("nonexistent@example.com")
    assert user is None

# Tests para create_user
def test_create_user_success(user_services, mock_user_repo, sample_user):
    mock_user_repo.get_by_email.return_value = None  # User does not exist
    mock_user_repo.create_user.return_value = sample_user
    
    created_user = user_services.create_user(sample_user)
    assert created_user == sample_user
    mock_user_repo.get_by_email.assert_called_once_with(sample_user.email)
    mock_user_repo.create_user.assert_called_once_with(sample_user)

def test_create_user_admin_role_forbidden(user_services, mock_user_repo, admin_user):
    with pytest.raises(HTTPException) as exc_info:
        user_services.create_user(admin_user)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Error: Inadmisible role admin"
    mock_user_repo.get_by_email.assert_not_called()
    mock_user_repo.create_user.assert_not_called()

def test_create_user_email_already_registered(user_services, mock_user_repo, sample_user):
    mock_user_repo.get_by_email.return_value = sample_user  # User already exists
    
    with pytest.raises(HTTPException) as exc_info:
        user_services.create_user(sample_user)
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Error: Email already registered"
    mock_user_repo.get_by_email.assert_called_once_with(sample_user.email)
    mock_user_repo.create_user.assert_not_called()

# Tests para modify_user
def test_modify_user_success(user_services, mock_user_repo, sample_user):
    modified_data = UserModifyDto(name="Updated Name", email="updated@example.com")
    
    # Create a copy of the user to simulate modification
    expected_user = sample_user.model_copy(deep=True)
    expected_user.name = modified_data.name
    expected_user.email = modified_data.email

    mock_user_repo.modify_user.return_value = expected_user

    result_user = user_services.modify_user(sample_user, modified_data)
    
    assert result_user.name == "Updated Name"
    assert result_user.email == "updated@example.com"
    mock_user_repo.modify_user.assert_called_once()
    # Verify that the user object passed to modify_user was updated
    assert mock_user_repo.modify_user.call_args[0][0].name == "Updated Name"
    assert mock_user_repo.modify_user.call_args[0][0].email == "updated@example.com"

def test_modify_user_partial_update(user_services, mock_user_repo, sample_user):
    modified_data = UserModifyDto(name="Only Name Changed", email=sample_user.email, hashed_password=sample_user.hashed_password)
    
    expected_user = sample_user.model_copy(deep=True)
    expected_user.name = modified_data.name

    mock_user_repo.modify_user.return_value = expected_user

    result_user = user_services.modify_user(sample_user, modified_data)
    
    assert result_user.name == "Only Name Changed"
    assert result_user.email == sample_user.email # Email should remain unchanged
    mock_user_repo.modify_user.assert_called_once()
    assert mock_user_repo.modify_user.call_args[0][0].name == "Only Name Changed"
    assert mock_user_repo.modify_user.call_args[0][0].email == sample_user.email
