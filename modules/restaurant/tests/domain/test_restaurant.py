from datetime import time
from uuid import uuid4
from modules.restaurant.domain.restaurant import Restaurant

def test_create_restaurant_model():
    restaurant = Restaurant(
        id=uuid4(),
        name="Test Restaurant",
        address="Test Address",
        opening_time=time(9, 0),
        closing_time=time(18, 0)
    )

    assert restaurant.name == "Test Restaurant"
    assert restaurant.opening_time < restaurant.closing_time
