from uuid import UUID
from typing import List
from modules.restaurant.domain.table import Table
from modules.restaurant.domain.table_repository_interface import ITableRepository
from modules.restaurant.application.dtos.table_dto import CreateTableDTO, TableDTO
from modules.restaurant.domain.exceptions import TableNumberConflictError

class TableServices:
    def __init__(self, table_repository: ITableRepository):
        self.table_repository = table_repository

    def create_table(self, table_dto: CreateTableDTO) -> TableDTO:
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
        return TableDTO.model_validate(table)

    def get_available_tables(self, restaurant_id: UUID, capacity: int, location: str) -> List[TableDTO]:
        tables = self.table_repository.get_available_tables(restaurant_id, capacity, location)
        return [TableDTO.model_validate(table) for table in tables]
