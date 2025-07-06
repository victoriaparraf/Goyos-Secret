from uuid import uuid4, UUID
from typing import List
from fastapi import HTTPException
from modules.restaurant.domain.restaurant_repository_interface import IRestaurantRepository
from modules.restaurant.domain.table_repository_interface import ITableRepository
from modules.restaurant.domain.restaurant import Restaurant
from modules.restaurant.application.dtos.restaurant_create_dto import CreateRestaurantDTO
from modules.restaurant.application.dtos.restaurant_update_dto import UpdateRestaurantDTO
from modules.restaurant.application.dtos.restaurant_response_dto import RestaurantResponseDto


class RestaurantService:
    def __init__(
        self,
        restaurant_repo: IRestaurantRepository,
        table_repo: ITableRepository
    ):
        self.restaurant_repo = restaurant_repo
        self.table_repo = table_repo

    def create_restaurant(self, dto: CreateRestaurantDTO) -> RestaurantResponseDto:
        # Validación: nombre único
        existing = self.restaurant_repo.get_by_name(dto.name)
        if existing:
            raise HTTPException(status_code=409, detail="Restaurant with this name already exists.")

        # Validación: horarios
        if dto.closing_time <= dto.opening_time:
            raise HTTPException(status_code=400, detail="Closing time must be after opening time.")

        restaurant = Restaurant(
            id=uuid4(),
            name=dto.name,
            address=dto.address,
            opening_time=dto.opening_time,
            closing_time=dto.closing_time
        )

        saved = self.restaurant_repo.save(restaurant)
        return RestaurantResponseDto(**saved.model_dump())

    def get_restaurant_by_id(self, restaurant_id: UUID) -> RestaurantResponseDto:
        restaurant = self.restaurant_repo.get_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found.")
        return RestaurantResponseDto(**restaurant.model_dump())

    def list_restaurants(self) -> List[RestaurantResponseDto]:
        restaurants = self.restaurant_repo.get_all()
        return [RestaurantResponseDto(**r.model_dump()) for r in restaurants]

    def update_restaurant(self, restaurant_id: UUID, dto: UpdateRestaurantDTO) -> RestaurantResponseDto:
        restaurant = self.restaurant_repo.get_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found.")

        # Validación: horario
        if dto.opening_time or dto.closing_time:
            opening = dto.opening_time or restaurant.opening_time
            closing = dto.closing_time or restaurant.closing_time
            if closing <= opening:
                raise HTTPException(status_code=400, detail="Closing time must be after opening time.")

        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(restaurant, field, value)

        updated = self.restaurant_repo.modify_restaurant(restaurant)
        return RestaurantResponseDto(**updated.model_dump())

    def delete_restaurant(self, restaurant_id: UUID) -> None:
        restaurant = self.restaurant_repo.get_by_id(restaurant_id)
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found.")

        tables = self.table_repo.get_by_restaurant_id(restaurant_id)
        if tables:
            raise HTTPException(status_code=400, detail="Cannot delete restaurant with existing tables.")

        self.restaurant_repo.delete(restaurant_id)
