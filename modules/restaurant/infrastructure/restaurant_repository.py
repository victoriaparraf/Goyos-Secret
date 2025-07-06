from typing import Optional
from uuid import UUID
from sqlmodel import Session, select
from modules.restaurant.domain.restaurant import Restaurant
from modules.restaurant.domain.restaurant_repository_interface import IRestaurantRepository
from modules.restaurant.infrastructure.restaurant_db_model import RestaurantDBModel, to_domain, to_db

class RestaurantRepository(IRestaurantRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, restaurant_id: UUID) -> Optional[Restaurant]:
        statement = select(RestaurantDBModel).where(RestaurantDBModel.uuid == restaurant_id)
        result = self.db.exec(statement).first()
        return to_domain(result) if result else None


    def get_by_name(self, name: str) -> Optional[Restaurant]:
        statement = select(RestaurantDBModel).where(RestaurantDBModel.name == name)
        result = self.db.exec(statement).first()
        return result

    def save(self, restaurant: Restaurant) -> Restaurant:
        restaurant_db = to_db(restaurant)
        self.db.add(restaurant_db)
        self.db.commit()
        self.db.refresh(restaurant_db)
        return to_domain(restaurant_db)

    def delete(self, restaurant_id: UUID) -> None:
        db_restaurant = self.db.get(RestaurantDBModel, restaurant_id)
        if db_restaurant:
            self.db.delete(db_restaurant)
            self.db.commit()
        
    def modify_restaurant(self, restaurant: Restaurant) -> Restaurant:
        db_restaurant = self.db.get(RestaurantDBModel, restaurant.id)
        if not db_restaurant:
            raise Exception("Restaurant not found")

        updated = to_db(restaurant)
        for field, value in updated.model_dump().items():
            setattr(db_restaurant, field, value)

        self.db.add(db_restaurant)
        self.db.commit()
        self.db.refresh(db_restaurant)
        return to_domain(db_restaurant)
