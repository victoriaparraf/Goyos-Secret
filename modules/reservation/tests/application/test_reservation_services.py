import pytest
from unittest.mock import Mock
from uuid import uuid4
from datetime import datetime, timedelta
from fastapi import HTTPException

from modules.reservation.application.reservation_services import ReservationService
from modules.reservation.application.dtos.reservation_create_dto import ReservationCreateDto
from modules.reservation.application.dtos.reservation_response_dto import ReservationResponseDto
from modules.reservation.domain.reservation import Reservation, ReservationStatus
from modules.reservation.domain.reservation_repository_interface import IReservationRepository
from modules.menu.domain.menu_repository_interface import MenuRepositoryInterface
from modules.restaurant.domain.table_repository_interface import ITableRepository
from modules.restaurant.domain.restaurant_repository_interface import IRestaurantRepository
from modules.menu.domain.menu_item import MenuItem

@pytest.fixture
def mock_reservation_repo():
    return Mock(spec=IReservationRepository)

@pytest.fixture
def mock_table_repo():
    return Mock(spec=ITableRepository)

@pytest.fixture
def mock_menu_repo():
    return Mock(spec=MenuRepositoryInterface)

@pytest.fixture
def mock_restaurant_repo():
    return Mock(spec=IRestaurantRepository)

@pytest.fixture
def reservation_service(mock_reservation_repo, mock_table_repo, mock_menu_repo, mock_restaurant_repo):
    return ReservationService(mock_reservation_repo, mock_table_repo, mock_menu_repo, mock_restaurant_repo)

@pytest.fixture
def sample_table():
    # Mock de una mesa existente
    mock_table = Mock()
    mock_table.id = uuid4()
    mock_table.restaurant_id = uuid4()
    return mock_table



class SimpleRestaurant:
    def __init__(self, name: str):
        self.name = name

@pytest.fixture
def sample_restaurant():
    # Mock de un restaurante existente
    return SimpleRestaurant(name="Test Restaurant Name")

@pytest.fixture
def sample_user_id():
    return uuid4()

# Test de Solapamiento
def test_create_reservation_overlapping_table_rejected(reservation_service, mock_reservation_repo, mock_table_repo, sample_table, sample_user_id):
    # Arrange
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)

    dto = ReservationCreateDto(
        table_id=sample_table.id,
        start_time=start_time,
        end_time=end_time,
        num_people=4,
        special_instructions=None,
        preordered_dishes=[]
    )

    mock_table_repo.get_by_id.return_value = sample_table
    mock_reservation_repo.get_active_by_user_and_time.return_value = None
    mock_reservation_repo.get_active_by_table_and_time.return_value = Reservation(
        uuid=uuid4(),
        user_id=uuid4(),
        table_id=sample_table.id,
        start_time=start_time,
        end_time=end_time,
        num_people=2,
        special_instructions=None,
        status=ReservationStatus.PENDING
    )

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        reservation_service.create_reservation(sample_user_id, dto)
    
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "This table is already reserved at that time."
    mock_reservation_repo.get_active_by_table_and_time.assert_called_once_with(dto.table_id, dto.start_time, dto.end_time)

# Test de Pre-orden Inválido
def test_create_reservation_invalid_preordered_dish_rejected(reservation_service, mock_reservation_repo, mock_table_repo, mock_menu_repo, sample_table, sample_user_id):
    # Arrange
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)
    invalid_dish_id = uuid4()

    dto = ReservationCreateDto(
        table_id=sample_table.id,
        start_time=start_time,
        end_time=end_time,
        num_people=2,
        special_instructions=None,
        preordered_dishes=[invalid_dish_id]
    )

    mock_table_repo.get_by_id.return_value = sample_table
    mock_reservation_repo.get_active_by_user_and_time.return_value = None
    mock_reservation_repo.get_active_by_table_and_time.return_value = None
    mock_menu_repo.get_all_by_restaurant.return_value = [] # No dishes available

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        reservation_service.create_reservation(sample_user_id, dto)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == f"Dish {invalid_dish_id} is not available for this restaurant."
    mock_menu_repo.get_all_by_restaurant.assert_called_once_with(sample_table.restaurant_id)

def test_create_reservation_too_many_preordered_dishes_rejected(reservation_service, mock_reservation_repo, mock_table_repo, mock_menu_repo, sample_table, sample_user_id):
    # Arrange
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)
    
    # Create more than 5 dish IDs
    too_many_dishes = [uuid4() for _ in range(6)]

    dto = ReservationCreateDto(
        table_id=sample_table.id,
        start_time=start_time,
        end_time=end_time,
        num_people=2,
        special_instructions=None,
        preordered_dishes=too_many_dishes
    )

    mock_table_repo.get_by_id.return_value = sample_table
    mock_reservation_repo.get_active_by_user_and_time.return_value = None
    mock_reservation_repo.get_active_by_table_and_time.return_value = None
    
    # Mock some available dishes, but not enough to cover the too_many_dishes list
    mock_menu_repo.get_all_by_restaurant.return_value = [
        MenuItem(id=too_many_dishes[0], name="Dish 1", description="", category="", price=10.0, available_stock=10, image_url="http://example.com/1"),
        MenuItem(id=too_many_dishes[1], name="Dish 2", description="", category="", price=10.0, available_stock=10, image_url="http://example.com/2"),
        MenuItem(id=too_many_dishes[2], name="Dish 3", description="", category="", price=10.0, available_stock=10, image_url="http://example.com/3"),
        MenuItem(id=too_many_dishes[3], name="Dish 4", description="", category="", price=10.0, available_stock=10, image_url="http://example.com/4"),
        MenuItem(id=too_many_dishes[4], name="Dish 5", description="", category="", price=10.0, available_stock=10, image_url="http://example.com/5"),
    ]

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        reservation_service.create_reservation(sample_user_id, dto)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Cannot pre-order more than 5 dishes."
    mock_menu_repo.get_all_by_restaurant.assert_not_called()


def test_create_reservation_success_with_preordered_dishes(reservation_service, mock_reservation_repo, mock_table_repo, mock_menu_repo, mock_restaurant_repo, sample_table, sample_user_id, sample_restaurant):
    # Arrange
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)
    
    dish_id_1 = uuid4()
    dish_id_2 = uuid4()

    dto = ReservationCreateDto(
        table_id=sample_table.id,
        start_time=start_time,
        end_time=end_time,
        num_people=2,
        special_instructions=None,
        preordered_dishes=[dish_id_1, dish_id_2]
    )

    mock_table_repo.get_by_id.return_value = sample_table
    mock_reservation_repo.get_active_by_user_and_time.return_value = None
    mock_reservation_repo.get_active_by_table_and_time.return_value = None
    mock_restaurant_repo.get_by_id.return_value = sample_restaurant
    
    mock_menu_repo.get_all_by_restaurant.return_value = [
        MenuItem(id=dish_id_1, name="Dish 1", description="", category="", price=10.0, available_stock=10, image_url="http://example.com/1"),
        MenuItem(id=dish_id_2, name="Dish 2", description="", category="", price=10.0, available_stock=10, image_url="http://example.com/2"),
    ]

    mock_reservation_repo.save.return_value = ReservationResponseDto(
        uuid=uuid4(),
        user_id=sample_user_id,
        table_id=sample_table.id,
        start_time=start_time,
        end_time=end_time,
        num_people=dto.num_people,
        special_instructions=None,
        status=ReservationStatus.PENDING,
        preordered_dishes=dto.preordered_dishes,
        restaurant_name=sample_restaurant.name
    )

    # Act
    response_dto = reservation_service.create_reservation(sample_user_id, dto)

    # Assert
    assert response_dto.table_id == dto.table_id
    assert response_dto.preordered_dishes == dto.preordered_dishes
    mock_reservation_repo.save.assert_called_once()
    mock_menu_repo.get_all_by_restaurant.assert_called_once_with(sample_table.restaurant_id)