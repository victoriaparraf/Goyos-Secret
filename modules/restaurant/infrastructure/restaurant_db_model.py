from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import uuid4,UUID
from modules.restaurant.domain.restaurant import Restaurant

class RestaurantDBModel(SQLModel, Restaurant, table=True):
    id: UUID = Field(default_factory=uuid4, index=True, primary_key=True)
    name: str
    address: str
    opening_time: str
    closing_time: str

def to_domain(restaurat_db: RestaurantDBModel) -> Restaurant:
    return Restaurant(
        uuid=restaurat_db.uuid,
        name=restaurat_db.name,
        address=restaurat_db.address,
        opening_time=restaurat_db.opening_time,
        closing_time=restaurat_db.closing_time
    )

def to_db(restaurant: Restaurant) -> RestaurantDBModel:
    return RestaurantDBModel(
        name=restaurant.name,
        address=restaurant.address,
        opening_time=restaurant.opening_time,
        closing_time=restaurant.closing_time
    )
