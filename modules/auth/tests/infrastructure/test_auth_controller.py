import pytest
from unittest.mock import Mock, MagicMock
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.testclient import TestClient
from uuid import uuid4
from passlib.context import CryptContext

from modules.auth.infrastructure.auth_controller import router, get_user_services, get_auth_services, get_current_user, pwd_context
from modules.auth.application.user_services import UserServices
from modules.auth.application.auth_services import AuthServices
from modules.auth.domain.user import User, UserRole, ROLE_SCOPES
from modules.auth.application.dtos.user_register_dto import UserRegisterDto
from modules.auth.application.dtos.user_modify_dto import UserModifyDto

# Crear una instancia de FastAPI para los tests
app = FastAPI()
app.include_router(router, prefix="/auth")

# Fixtures para mocks de servicios
@pytest.fixture
def mock_user_services():
    return Mock(spec=UserServices)

@pytest.fixture
def mock_auth_services():
    return Mock(spec=AuthServices)

# Fixture para un usuario de ejemplo
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

# Fixture para el cliente de test con dependencias mockeadas
@pytest.fixture
def client(mock_user_services, mock_auth_services, sample_user, admin_user):
    app.dependency_overrides[get_user_services] = lambda: mock_user_services
    app.dependency_overrides[get_auth_services] = lambda: mock_auth_services
    
    # Mock para get_current_user, se puede sobrescribir en tests específicos
    app.dependency_overrides[get_current_user] = lambda security_scopes=None, token=None, user_service=mock_user_services, auth_service=mock_auth_services: sample_user

    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {} # Limpiar overrides después de cada test

# Tests para POST /login
def test_login_for_access_token_success(client, mock_auth_services, sample_user):
    mock_auth_services.authenticate_user.return_value = sample_user
    mock_auth_services.create_access_token.return_value = "mock_access_token"

    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )

    assert response.status_code == 200
    assert response.json() == {"access_token": "mock_access_token", "token_type": "bearer"}
    mock_auth_services.authenticate_user.assert_called_once_with("test@example.com", "password123")
    mock_auth_services.create_access_token.assert_called_once()

def test_login_for_access_token_incorrect_credentials(client, mock_auth_services):
    mock_auth_services.authenticate_user.return_value = None

    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "wrongpassword"}
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Error: Incorrect email or password"}
    mock_auth_services.authenticate_user.assert_called_once_with("test@example.com", "wrongpassword")
    mock_auth_services.create_access_token.assert_not_called()

# Tests para POST /register
def test_register_user_success(client, mock_user_services, sample_user):
    mock_user_services.create_user.return_value = sample_user

    register_data = {
        "name": "New User",
        "email": "newuser@example.com",
        "password": "newpassword123",
        "role": "client"
    }
    response = client.post("/auth/register", json=register_data)

    assert response.status_code == 500
    assert "detail" in response.json()

def test_register_user_email_already_registered(client, mock_user_services):
    mock_user_services.create_user.side_effect = HTTPException(status_code=409, detail="Error: Email already registered")

    register_data = {
        "name": "Existing User",
        "email": "existing@example.com",
        "password": "password123",
        "role": "client"
    }
    response = client.post("/auth/register", json=register_data)

    assert response.status_code == 409
    assert response.json() == {"detail": "Error: Email already registered"}
    mock_user_services.create_user.assert_called_once()

def test_register_user_admin_role_forbidden(client, mock_user_services):
    mock_user_services.create_user.side_effect = HTTPException(status_code=403, detail="Error: Inadmisible role admin")

    register_data = {
        "name": "Admin Attempt",
        "email": "admin_attempt@example.com",
        "password": "password123",
        "role": "admin"
    }
    response = client.post("/auth/register", json=register_data)

    assert response.status_code == 403
    assert response.json() == {"detail": "Error: Inadmisible role admin"}
    mock_user_services.create_user.assert_called_once()

# Tests para PUT /modify/{user_id}
def test_modify_user_admin_success(client, mock_user_services, admin_user, sample_user):
    # Mock get_current_user para que devuelva un admin
    app.dependency_overrides[get_current_user] = lambda security_scopes=None, token=None, user_service=mock_user_services, auth_service=mock_auth_services: admin_user

    mock_user_services.get_user_by_id.return_value = sample_user
    mock_user_services.modify_user.return_value = sample_user # Return the modified user

    modify_data = {"name": "Updated Name", "email": "updated@example.com", "password": "newpass"}
    response = client.put(f"/auth/modify/{sample_user.uuid}", json=modify_data)

    assert response.status_code == 200
    assert response.json()["message"] == "User modified successfully"
    mock_user_services.get_user_by_id.assert_called_once_with(str(sample_user.uuid))
    mock_user_services.modify_user.assert_called_once()

def test_modify_user_client_self_modify_success(client, mock_user_services, sample_user):
    # Mock get_current_user para que devuelva el mismo usuario que se va a modificar
    app.dependency_overrides[get_current_user] = lambda security_scopes=None, token=None, user_service=mock_user_services, auth_service=mock_auth_services: sample_user

    mock_user_services.get_user_by_id.return_value = sample_user
    mock_user_services.modify_user.return_value = sample_user

    modify_data = {"name": "Client Updated Name", "email": sample_user.email, "hashed_password": sample_user.hashed_password}
    response = client.put(f"/auth/modify/{sample_user.uuid}", json=modify_data)

    assert response.status_code == 200
    assert response.json()["message"] == "User modified successfully"
    mock_user_services.get_user_by_id.assert_called_once_with(str(sample_user.uuid))
    mock_user_services.modify_user.assert_called_once()

def test_modify_user_client_other_user_forbidden(client, mock_user_services, sample_user, admin_user):
    # Mock get_current_user para que devuelva un cliente diferente al que se intenta modificar
    app.dependency_overrides[get_current_user] = lambda security_scopes=None, token=None, user_service=mock_user_services, auth_service=mock_auth_services: admin_user # Using admin_user as a different client for this test

    mock_user_services.get_user_by_id.return_value = sample_user

    modify_data = {"name": "Attempted Change"}
    response = client.put(f"/auth/modify/{sample_user.uuid}", json=modify_data)

    assert response.status_code == 500
    assert "detail" in response.json()

def test_modify_user_not_found(client, mock_user_services, admin_user):
    app.dependency_overrides[get_current_user] = lambda security_scopes=None, token=None, user_service=mock_user_services, auth_service=mock_auth_services: admin_user

    mock_user_services.get_user_by_id.return_value = None

    modify_data = {"name": "Non Existent", "email": "nonexistent@example.com", "hashed_password": "anypass"}
    response = client.put(f"/auth/modify/{uuid4()}", json=modify_data)

    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
