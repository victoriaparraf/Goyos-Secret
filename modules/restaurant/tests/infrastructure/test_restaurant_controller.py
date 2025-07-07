import pytest
from fastapi.testclient import TestClient
from datetime import time
from uuid import uuid4
from fastapi import FastAPI
from unittest.mock import Mock
from modules.restaurant.infrastructure.restaurant_controller import router, get_restaurant_service
from modules.auth.infrastructure.auth_controller import get_current_user
from modules.restaurant.application.restaurant_services import RestaurantService
from modules.auth.domain.user import User, UserRole

app = FastAPI()
app.include_router(router, prefix="/restaurants")

@pytest.fixture
def admin_user():
    return User(
        uuid=uuid4(),
        name="Admin",
        email="admin@example.com",
        hashed_password="hashed",
        role=UserRole.ADMIN
    )

@pytest.fixture
def mock_service():
    return Mock(spec=RestaurantService)

@pytest.fixture
def client(admin_user, mock_service):
    app.dependency_overrides[get_restaurant_service] = lambda: mock_service
    app.dependency_overrides[get_current_user] = lambda: admin_user
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}

def test_admin_can_create_restaurant(client, mock_service):
    mock_service.create_restaurant.return_value = {
        "id": str(uuid4()),
        "name": "Nuevo REST",
        "address": "Calle 123",
        "opening_time": time(8, 0),
        "closing_time": time(17, 0)
    }

    response = client.post("/restaurants/", json={
        "name": "Nuevo REST",
        "address": "Calle 123",
        "opening_time": "08:00:00",
        "closing_time": "17:00:00"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Nuevo REST"