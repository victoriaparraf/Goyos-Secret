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
        description="",
        category="",
        price=10.0,
        available_stock=10,
        image_url=""
    )
    new_menu_item = MenuItem(
        id=uuid4(),
        name="Existing Dish",
        description="",
        category="",
        price=12.0,
        available_stock=5,
        image_url=""
    )

    mock_menu_repo.get_menu_item_by_name.return_value = existing_menu_item

    with pytest.raises(HTTPException) as exc_info:
        menu_service.create_menu_item(new_menu_item)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Menu item with this name already exists."
    mock_menu_repo.get_menu_item_by_name.assert_called_once_with("Existing Dish")
    mock_menu_repo.create_menu_item.assert_not_called()

def test_create_menu_item_success(menu_service, mock_menu_repo):
    new_menu_item = MenuItem(
        id=uuid4(),
        name="New Dish",
        description="",
        category="",
        price=10.0,
        available_stock=10,
        image_url=""
    )

    mock_menu_repo.get_menu_item_by_name.return_value = None
    mock_menu_repo.create_menu_item.return_value = new_menu_item

    created_item = menu_service.create_menu_item(new_menu_item)

    assert created_item == new_menu_item
    mock_menu_repo.get_menu_item_by_name.assert_called_once_with("New Dish")
    mock_menu_repo.create_menu_item.assert_called_once_with(new_menu_item)
