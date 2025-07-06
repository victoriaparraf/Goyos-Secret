from typing import Optional
from uuid import UUID
from sqlmodel import Session, select
from modules.restaurant.domain.restaurant import Restaurant
from modules.restaurant.domain.restaurant_repository_interface import IRestaurantRepository
from modules.restaurant.infrastructure.restaurant_db_model import RestaurantDBModel

class RestaurantRepository(IRestaurantRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, restaurant_id: UUID) -> Optional[Restaurant]:
        statement = select(RestaurantDBModel).where(RestaurantDBModel.uuid == restaurant_id)
        result = self.db.exec(statement).first()
        return result

    def get_by_name(self, name: str) -> Optional[Restaurant]:
        statement = select(RestaurantDBModel).where(RestaurantDBModel.name == name)
        result = self.db.exec(statement).first()
        return result

    def save(self, restaurant: Restaurant) -> Restaurant:
        self.db.add(restaurant)
        self.db.commit()
        self.db.refresh(restaurant)

    def delete(self, restaurant: Restaurant) -> Restaurant:
        self.session.delete(restaurant)
        self.session.commit()
