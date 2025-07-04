from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from modules.restaurant.domain.restaurant import Restaurant
from modules.restaurant.domain.restaurant_repository_interface import IRestaurantRepository
from modules.restaurant.infrastructure.restaurant_db_model import RestaurantDBModel

class RestaurantRepository(IRestaurantRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, restaurant_id: UUID) -> Optional[Restaurant]:
        restaurant_db = self.session.query(RestaurantDBModel).filter_by(id=restaurant_id).first()
        return Restaurant.model_validate(restaurant_db) if restaurant_db else None

    def get_by_name(self, name: str) -> Optional[Restaurant]:
        restaurant_db = self.session.query(RestaurantDBModel).filter_by(name=name).first()
        return Restaurant.model_validate(restaurant_db) if restaurant_db else None

    def save(self, restaurant: Restaurant) -> None:
        restaurant_db = self.session.query(RestaurantDBModel).filter_by(id=restaurant.id).first()
        if restaurant_db:
            restaurant_db.name = restaurant.name
            restaurant_db.location = restaurant.location
            restaurant_db.opening_time = restaurant.opening_time
            restaurant_db.closing_time = restaurant.closing_time
        else:
            restaurant_db = RestaurantDBModel(**restaurant.model_dump())
            self.session.add(restaurant_db)
        self.session.commit()

    def delete(self, restaurant_id: UUID) -> None:
        restaurant_db = self.session.query(RestaurantDBModel).filter_by(id=restaurant_id).first()
        if restaurant_db:
            self.session.delete(restaurant_db)
            self.session.commit()
