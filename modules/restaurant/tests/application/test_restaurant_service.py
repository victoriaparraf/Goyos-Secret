import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import time
from fastapi import HTTPException
from modules.restaurant.application.restaurant_services import RestaurantService
from modules.restaurant.application.dtos.restaurant_create_dto import CreateRestaurantDTO
from modules.restaurant.domain.restaurant_repository_interface import IRestaurantRepository
from modules.restaurant.domain.table_repository_interface import ITableRepository
from modules.restaurant.domain.restaurant import Restaurant


@pytest.fixture
def mock_restaurant_repo():
    return Mock(spec=IRestaurantRepository)

@pytest.fixture
def mock_table_repo():
    return Mock(spec=ITableRepository)

@pytest.fixture
def restaurant_service(mock_restaurant_repo, mock_table_repo):
    return RestaurantService(mock_restaurant_repo, mock_table_repo)


def test_create_restaurant_fails_when_name_exists(restaurant_service, mock_restaurant_repo):
    dto = CreateRestaurantDTO(
        name="Restaurante X",
        address="Calle A",
        opening_time=time(9, 0),
        closing_time=time(18, 0)
    )

    mock_restaurant_repo.get_by_name.return_value = Restaurant(
        id=uuid4(),
        name=dto.name,
        address=dto.address,
        opening_time=dto.opening_time,
        closing_time=dto.closing_time
    )

    with pytest.raises(HTTPException) as exc_info:
        restaurant_service.create_restaurant(dto)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Restaurant with this name already exists."


def test_create_restaurant_fails_when_closing_before_opening(restaurant_service, mock_restaurant_repo):
    dto = CreateRestaurantDTO(
        name="Restaurante Invalido",
        address="Calle B",
        opening_time=time(18, 0),
        closing_time=time(9, 0)
    )

    mock_restaurant_repo.get_by_name.return_value = None  # No existe, pasa la validación de nombre

    with pytest.raises(HTTPException) as exc_info:
        restaurant_service.create_restaurant(dto)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Closing time must be after opening time."


def test_create_restaurant_success(restaurant_service, mock_restaurant_repo):
    dto = CreateRestaurantDTO(
        name="Restaurante Nuevo",
        address="Calle C",
        opening_time=time(9, 0),
        closing_time=time(18, 0)
    )

    mock_restaurant_repo.get_by_name.return_value = None

    # Simulamos que el repo devuelve el mismo restaurante que se guarda
    def fake_save(r: Restaurant):
        return r

    mock_restaurant_repo.save.side_effect = fake_save

    result = restaurant_service.create_restaurant(dto)

    assert result.name == dto.name
    assert result.address == dto.address
    assert result.opening_time == dto.opening_time
    assert result.closing_time == dto.closing_time
    mock_restaurant_repo.get_by_name.assert_called_once_with(dto.name)
    mock_restaurant_repo.save.assert_called_once()
