from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from modules.restaurant.domain.restaurant import Restaurant
from datetime import datetime

class RestaurantDBModel(SQLModel, Restaurant, table=True):
    id: UUID = Field(default_factory=uuid4, index=True, primary_key=True)
    name: str
    address: str
    opening_time: str
    closing_time: str

def _parse_time_string(time_str: str):
    # Remove timezone information if present
    if '+' in time_str:
        time_str = time_str.split('+')[0]
    elif '-' in time_str and len(time_str.split('-')) > 2: # Handle negative timezone offset, but not negative time
        time_str = time_str.rsplit('-', 1)[0]

    formats = ["%H:%M:%S.%f", "%H:%M:%S", "%H:%M"]
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue
    raise ValueError(f"Unable to parse time string: {time_str}")

def to_domain(restaurat_db: RestaurantDBModel) -> Restaurant:
    return Restaurant(
        id=restaurat_db.id,
        name=restaurat_db.name,
        address=restaurat_db.address,
        opening_time=_parse_time_string(restaurat_db.opening_time),
        closing_time=_parse_time_string(restaurat_db.closing_time)
    )

def to_db(restaurant: Restaurant) -> RestaurantDBModel:
    return RestaurantDBModel(
        id=restaurant.id,
        name=restaurant.name,
        address=restaurant.address,
        opening_time=str(restaurant.opening_time),
        closing_time=str(restaurant.closing_time)
    )
