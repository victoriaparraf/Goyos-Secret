from uuid import UUID
from typing import List
from modules.restaurant.domain.table import Table
from modules.restaurant.domain.table_repository_interface import ITableRepository
from modules.restaurant.application.dtos.table_create_dto import CreateTableDTO
from modules.restaurant.application.dtos.table_update_dto import UpdateTableDTO
from modules.restaurant.domain.exceptions import TableNumberConflictError

class TableServices:
    def __init__(self, table_repository: ITableRepository):
        self.table_repository = table_repository

    def create_table(self, table_dto: CreateTableDTO, current_user) -> CreateTableDTO:
        # Solo admin puede crear mesas
        if not hasattr(current_user, "role") or getattr(current_user, "role", None) != "admin":
            raise PermissionError("Solo los administradores pueden crear mesas.")

        # Validar capacidad
        if table_dto.capacity < 2 or table_dto.capacity > 12:
            raise ValueError("La capacidad de la mesa debe ser entre 2 y 12 personas.")

        # Validar unicidad de numero de mesa
        existing_table = self.table_repository.get_by_restaurant_and_table_number(
            table_dto.restaurant_id, table_dto.table_number
        )
        if existing_table:
            raise TableNumberConflictError("Ya existe una mesa con este número en el restaurante.")

        table = Table.create(
            restaurant_id=table_dto.restaurant_id,
            table_number=table_dto.table_number,
            capacity=table_dto.capacity,
            location=table_dto.location
        )
        self.table_repository.save(table)
        return CreateTableDTO.model_validate(table)

    def get_available_tables(self, restaurant_id: UUID, capacity: int, location: str) -> List[TableDTO]:
        # Filtrar por capacidad y ubicación
        tables = self.table_repository.get_available_tables(restaurant_id, capacity, location)
        return [CreateTableDTO.model_validate(table) for table in tables]
