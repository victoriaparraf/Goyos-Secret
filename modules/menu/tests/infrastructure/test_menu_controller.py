import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from uuid import uuid4
from fastapi import FastAPI

from modules.menu.infrastructure.menu_controller import router, get_menu_repository
from modules.auth.infrastructure.auth_controller import get_current_user
from modules.menu.application.menu_services import MenuServices
from modules.auth.domain.user import User, UserRole
from modules.menu.domain.menu_item import MenuItem

app = FastAPI()
app.include_router(router, prefix="/menu")

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
def client_user():
    return User(
        uuid=uuid4(),
        name="Client",
        email="client@example.com",
        hashed_password="hashed",
        role=UserRole.CLIENT
    )

@pytest.fixture
def mock_menu_services():
    return Mock(spec=MenuServices)

@pytest.fixture
def test_client(mock_menu_services):
    app.dependency_overrides[get_menu_repository] = lambda: mock_menu_services
    app.dependency_overrides[get_current_user] = lambda: admin_user() # Default to admin
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}

@patch('modules.menu.infrastructure.menu_controller.MenuServices')
def test_admin_can_create_menu_item(mock_menu_services_class, test_client, admin_user):
    app.dependency_overrides[get_current_user] = lambda: admin_user
    
    test_restaurant_id = uuid4()
    mock_service_instance = mock_menu_services_class.return_value
    mock_service_instance.create_menu_item.return_value = MenuItem(
        id=uuid4(),
        name="Test Dish",
        description="A test dish",
        category="Appetizer",
        price=10.0,
        available_stock=10,
        image_url="http://example.com/dish.jpg",
        restaurant_id=test_restaurant_id
    )

    response = test_client.post("/menu/menu-item", json={
        "id": str(uuid4()),
        "name": "Test Dish",
        "description": "A test dish",
        "category": "Appetizer",
        "price": 10.0,
        "available_stock": 10,
        "image_url": "http://example.com/dish.jpg",
        "restaurant_id": str(test_restaurant_id)
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Menu item created successfully"
    mock_service_instance.create_menu_item.assert_called_once_with(
        name="Test Dish",
        description="A test dish",
        category="Appetizer",
        price=10.0,
        available_stock=10,
        restaurant_id=test_restaurant_id,
        image_url="http://example.com/dish.jpg"
    )

def test_client_cannot_create_menu_item(test_client, mock_menu_services, client_user):
    app.dependency_overrides[get_current_user] = lambda: client_user

    response = test_client.post("/menu/menu-item", json={
        "id": str(uuid4()),
        "name": "Client Dish",
        "description": "A client dish",
        "category": "Main",
        "price": 15.0,
        "available_stock": 5,
        "image_url": "http://example.com/client_dish.jpg",
        "restaurant_id": str(uuid4())
    })

    assert response.status_code == 403
    assert response.json()["detail"] == "Only admins can create menu items."
    mock_menu_services.create_menu_item.assert_not_called()
