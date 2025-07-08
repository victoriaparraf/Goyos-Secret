import pytest
from unittest.mock import Mock
from uuid import uuid4
from fastapi import HTTPException

from modules.restaurant.application.table_services import TableService
from modules.restaurant.application.dtos.table_create_dto import CreateTableDTO
from modules.restaurant.domain.table_repository_interface import ITableRepository
from modules.restaurant.domain.table import Table

@pytest.fixture
def mock_table_repo():
    return Mock(spec=ITableRepository)

@pytest.fixture
def table_service(mock_table_repo):
    return TableService(mock_table_repo)

def test_create_table_capacity_1_rejected(table_service, mock_table_repo):
    dto = CreateTableDTO(
        restaurant_id=uuid4(),
        number=1,
        capacity=1,
        location="Indoor"
    )
    with pytest.raises(HTTPException) as exc_info:
        table_service.create_table(dto)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Table capacity cannot be 1 or 13."
    mock_table_repo.get_by_restaurant_and_table_number.assert_not_called()
    mock_table_repo.save.assert_not_called()

def test_create_table_capacity_13_rejected(table_service, mock_table_repo):
    dto = CreateTableDTO(
        restaurant_id=uuid4(),
        number=2,
        capacity=13,
        location="Outdoor"
    )
    with pytest.raises(HTTPException) as exc_info:
        table_service.create_table(dto)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Table capacity cannot be 1 or 13."
    mock_table_repo.get_by_restaurant_and_table_number.assert_not_called()
    mock_table_repo.save.assert_not_called()

def test_create_table_capacity_valid(table_service, mock_table_repo):
    restaurant_id = uuid4()
    dto = CreateTableDTO(
        restaurant_id=restaurant_id,
        number=3,
        capacity=4,
        location="Terrace"
    )
    
    mock_table_repo.get_by_restaurant_and_table_number.return_value = None
    mock_table_repo.save.return_value = Table(
        id=uuid4(),
        restaurant_id=restaurant_id,
        number=dto.number,
        capacity=dto.capacity,
        location=dto.location
    )

    response_dto = table_service.create_table(dto)
    assert response_dto.capacity == 4
    mock_table_repo.get_by_restaurant_and_table_number.assert_called_once_with(dto.restaurant_id, dto.number)
    mock_table_repo.save.assert_called_once()
