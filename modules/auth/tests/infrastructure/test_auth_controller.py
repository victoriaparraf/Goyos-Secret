
import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from fastapi.testclient import TestClient
from fastapi import FastAPI
from modules.auth.infrastructure.auth_controller import router as auth_router, get_auth_services, get_user_services
from modules.auth.application.auth_services import AuthServices
from modules.auth.application.user_services import UserServices


app = FastAPI()
app.include_router(auth_router, prefix="/auth")

@pytest.fixture
def mock_auth_services():
    return Mock(spec=AuthServices)

@pytest.fixture
def mock_user_services():
    return Mock(spec=UserServices)

@pytest.fixture(autouse=True)
def override_dependencies(mock_auth_services, mock_user_services):
    app.dependency_overrides[get_auth_services] = lambda: mock_auth_services
    app.dependency_overrides[get_user_services] = lambda: mock_user_services
    yield
    app.dependency_overrides = {}

@pytest.fixture
def client():
    return TestClient(app)

def test_register_user_with_admin_role_forbidden(client, mock_user_services):
    mock_user_services.create_user.side_effect = HTTPException(
        status_code=403,
        detail="Error: Inadmisible role admin"
    )
    
    response = client.post("/auth/register", json={
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "adminpass",
        "role": "admin"
    })
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Error: Inadmisible role admin"

def test_login_for_access_token_incorrect_credentials(client, mock_auth_services):
    mock_auth_services.authenticate_user.return_value = None
    
    response = client.post("/auth/login", data={
        "username": "wrong@example.com",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Error: Incorrect email or password"
