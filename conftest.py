import pytest

# Import all DB models to ensure they are registered with SQLModel.metadata
from modules.auth.infrastructure.user_db_model import UserDB
from modules.menu.infrastructure.menu_item_db_model import MenuItemDB
from modules.menu.infrastructure.pre_order_item_db_model import PreOrderItemDB
from modules.reservation.infrastructure.reservation_db_model import ReservationDBModel
from modules.restaurant.infrastructure.restaurant_db_model import RestaurantDBModel
from modules.restaurant.infrastructure.table_db_model import TableDBModel

@pytest.fixture(scope="session", autouse=True)
def load_all_db_models():
    """Ensures all DB models are loaded and registered with SQLModel.metadata."""
    pass
