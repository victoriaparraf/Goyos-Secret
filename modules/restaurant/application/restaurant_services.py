from uuid import UUID
from modules.restaurant.domain.restaurant import Restaurant
from modules.restaurant.domain.restaurant_repository_interface import IRestaurantRepository
from modules.restaurant.domain.table_repository_interface import ITableRepository
from modules.restaurant.application.dtos.restaurant_create_dto import CreateRestaurantDTO
from modules.restaurant.application.dtos.restaurant_update_dto import UpdateRestaurantDTO
from modules.auth.application.auth_services import User  
from modules.restaurant.domain.exceptions import (
    RestaurantAlreadyExistsError,
    RestaurantNotFoundError,
    CannotDeleteRestaurantWithTablesError,
)

class RestaurantServices:
    def __init__(self, restaurant_repository: IRestaurantRepository, table_repository: ITableRepository):
        self.restaurant_repository = restaurant_repository
        self.table_repository = table_repository

    def create_restaurant(self, restaurant_dto: CreateRestaurantDTO, current_user: User) -> CreateRestaurantDTO:
        # Solo admin puede crear
        if not hasattr(current_user, "role") or getattr(current_user, "role", None) != "admin":
            raise PermissionError("Solo los administradores pueden crear restaurantes.")

        # Validar campos obligatorios (asumimos que el DTO ya valida presencia, pero validamos horario aquí)
        if restaurant_dto.opening_time >= restaurant_dto.closing_time:
            raise ValueError("La hora de cierre debe ser mayor a la hora de apertura.")

        # Validar nombre único
        existing_restaurant = self.restaurant_repository.get_by_name(restaurant_dto.name)
        if existing_restaurant:
            raise RestaurantAlreadyExistsError("Ya existe un restaurante con este nombre.")

        # Crear entidad
        restaurant = Restaurant(
            name=restaurant_dto.name,
            location=restaurant_dto.location,
            opening_time=restaurant_dto.opening_time,
            closing_time=restaurant_dto.closing_time
        )
        self.restaurant_repository.save(restaurant)
        # Retornar DTO de respuesta
        return CreateRestaurantDTO.model_validate(restaurant)

    def update_restaurant(self, restaurant_id: UUID, restaurant_dto: UpdateRestaurantDTO, current_user: User) -> UpdateRestaurantDTO:
        # Solo admin puede editar
        if not hasattr(current_user, "role") or getattr(current_user, "role", None) != "admin":
            raise PermissionError("Solo los administradores pueden modificar restaurantes.")

        restaurant = self.restaurant_repository.get_by_id(restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundError("Restaurante no encontrado.")

        # No se puede cambiar el id (no modificar restaurant_id)
        # Validar horario
        if restaurant_dto.opening_time >= restaurant_dto.closing_time:
            raise ValueError("La hora de cierre debe ser mayor a la hora de apertura.")

        # Actualizar campos permitidos
        restaurant.name = restaurant_dto.name
        restaurant.location = restaurant_dto.location
        restaurant.opening_time = restaurant_dto.opening_time
        restaurant.closing_time = restaurant_dto.closing_time

        self.restaurant_repository.save(restaurant)
        return UpdateRestaurantDTO.model_validate(restaurant)

    def delete_restaurant(self, restaurant_id: UUID, current_user: User) -> None:
        # Solo admin puede eliminar
        if not hasattr(current_user, "role") or getattr(current_user, "role", None) != "admin":
            raise PermissionError("Solo los administradores pueden eliminar restaurantes.")

        # Verificar que el restaurante existe
        restaurant = self.restaurant_repository.get_by_id(restaurant_id)
        if not restaurant:
            raise RestaurantNotFoundError("Restaurante no encontrado.")

        # No se puede eliminar si tiene mesas asociadas
        tables = self.table_repository.get_by_restaurant_id(restaurant_id)
        if tables and len(tables) > 0:
            raise CannotDeleteRestaurantWithTablesError("No se puede eliminar un restaurante con mesas asociadas.")

        self.restaurant_repository.delete(restaurant_id)
