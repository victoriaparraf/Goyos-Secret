import pytest
from unittest.mock import Mock
from uuid import uuid4
from fastapi import HTTPException

from modules.menu.application.menu_services import MenuServices
from modules.menu.domain.menu_repository_interface import MenuRepositoryInterface
from modules.menu.domain.menu_item import MenuItem

@pytest.fixture
def mock_menu_repo():
    return Mock(spec=MenuRepositoryInterface)

@pytest.fixture
def menu_service(mock_menu_repo):
    return MenuServices(mock_menu_repo)

def test_create_menu_item_name_already_exists(menu_service, mock_menu_repo):
    existing_menu_item = MenuItem(
        id=uuid4(),
        name="Existing Dish",
        description="A test description",
        category="Test Category",
        price=10.0,
        available_stock=10,
        image_url="",
        restaurant_id=uuid4()
    )
    new_menu_item = MenuItem(
        id=uuid4(),
        name="Existing Dish",
        description="A test description",
        category="Test Category",
        price=12.0,
        available_stock=5,
        image_url="",
        restaurant_id=uuid4()
    )

    mock_menu_repo.get_all_by_restaurant.return_value = [existing_menu_item]

    with pytest.raises(HTTPException) as exc_info:
        menu_service.create_menu_item(
            name=new_menu_item.name,
            description=new_menu_item.description,
            category=new_menu_item.category,
            price=new_menu_item.price,
            available_stock=new_menu_item.available_stock,
            restaurant_id=new_menu_item.restaurant_id,
            image_url=new_menu_item.image_url
        )

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Menu item with this name already exists in this restaurant."
    mock_menu_repo.get_all_by_restaurant.assert_called_once_with(new_menu_item.restaurant_id)
    mock_menu_repo.create_menu_item.assert_not_called()

def test_create_menu_item_success(menu_service, mock_menu_repo):
    new_menu_item = MenuItem(
        id=uuid4(),
        name="New Dish",
        description="A new test description",
        category="New Test Category",
        price=10.0,
        available_stock=10,
        image_url="",
        restaurant_id=uuid4()
    )

    mock_menu_repo.get_all_by_restaurant.return_value = []
    mock_menu_repo.create_menu_item.return_value = new_menu_item

    created_item = menu_service.create_menu_item(
        name=new_menu_item.name,
        description=new_menu_item.description,
        category=new_menu_item.category,
        price=new_menu_item.price,
        available_stock=new_menu_item.available_stock,
        restaurant_id=new_menu_item.restaurant_id,
        image_url=new_menu_item.image_url
    )

    assert created_item == new_menu_item
    mock_menu_repo.get_all_by_restaurant.assert_called_once_with(new_menu_item.restaurant_id)
    mock_menu_repo.create_menu_item.assert_called_once()
    called_item = mock_menu_repo.create_menu_item.call_args[0][0]
    assert called_item.name == new_menu_item.name
    assert called_item.description == new_menu_item.description
    assert called_item.category == new_menu_item.category
    assert called_item.price == new_menu_item.price
    assert called_item.available_stock == new_menu_item.available_stock
    assert called_item.restaurant_id == new_menu_item.restaurant_id
    assert called_item.image_url == new_menu_item.image_url
