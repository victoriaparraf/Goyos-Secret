from uuid import UUID
from modules.restaurant.domain.restaurant import Restaurant
from modules.restaurant.domain.restaurant_repository_interface import IRestaurantRepository
from modules.restaurant.domain.table_repository_interface import ITableRepository
from modules.restaurant.application.dtos.restaurant_dto import CreateRestaurantDTO, UpdateRestaurantDTO, RestaurantDTO
from modules.auth.application.auth_services import get_current_user, User  # Asumiendo que existe
from modules.restaurant.domain.exceptions import (
    RestaurantAlreadyExistsError,
    RestaurantNotFoundError,
    CannotDeleteRestaurantWithTablesError,
)

class RestaurantServices:
    def __init__(self, restaurant_repository: IRestaurantRepository, table_repository: ITableRepository):
        self.restaurant_repository = restaurant_repository
        self.table_repository = table_repository

    def create_restaurant(self, restaurant_dto: CreateRestaurantDTO, current_user: User) -> RestaurantDTO:
        if not current_user.is_admin:
            raise PermissionError("Solo los administradores pueden crear restaurantes.")

        existing_restaurant = self.restaurant_repository.get_by_name(restaurant_dto.name)
        if existing_restaurant:
            raise RestaurantAlreadyExistsError("Ya existe un restaurante con este nombre.")

        restaurant = Restaurant.create(
            name=restaurant_dto.name,
            location=restaurant_dto.location,
            opening_time=restaurant_dto.opening_time,
            closing_time=restaurant_dto.closing_time
        )
        self.restaurant_repository.save(restaurant)
        return RestaurantDTO.model_validate(restaurant)

    def update_restaurant(self, restaurant_id: UUID, restaurant_dto: UpdateRestaurantDTO, current_user: User) -> RestaurantDTO:
        if not current_user.is_admin:
            raise PermissionError("Solo los administradores pueden modificar restaurantes.")

        restaurant = self.restaurant_repository.get_by_id(restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundError("Restaurante no encontrado.")

        restaurant.name = restaurant_dto.name
        restaurant.location = restaurant_dto.location
        restaurant.opening_time = restaurant_dto.opening_time
        restaurant.closing_time = restaurant_dto.closing_time
        
        if restaurant.opening_time >= restaurant.closing_time:
            raise ValueError("La hora de apertura debe ser anterior a la hora de cierre.")

        self.restaurant_repository.save(restaurant)
        return RestaurantDTO.model_validate(restaurant)

    def delete_restaurant(self, restaurant_id: UUID, current_user: User) -> None:
        if not current_user.is_admin:
            raise PermissionError("Solo los administradores pueden eliminar restaurantes.")

        tables = self.table_repository.get_by_restaurant_id(restaurant_id)
        if tables:
            raise CannotDeleteRestaurantWithTablesError("No se puede eliminar un restaurante con mesas asociadas.")

        self.restaurant_repository.delete(restaurant_id)
