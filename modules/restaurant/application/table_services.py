from uuid import uuid4, UUID
from fastapi import HTTPException
from typing import List
from modules.restaurant.domain.table_repository_interface import ITableRepository
from modules.restaurant.domain.table import Table
from modules.restaurant.application.dtos.table_create_dto import CreateTableDTO
from modules.restaurant.application.dtos.table_update_dto import UpdateTableDTO
from modules.restaurant.application.dtos.table_response_dto import TableResponseDto


class TableService:
    def __init__(self, table_repo: ITableRepository):
        self.table_repo = table_repo

    def create_table(self, dto: CreateTableDTO) -> TableResponseDto:
        if dto.capacity == 1 or dto.capacity == 13:
            raise HTTPException(status_code=400, detail="Table capacity cannot be 1 or 13.")

        # Validar duplicado de número de mesa en el restaurante
        existing = self.table_repo.get_by_restaurant_and_table_number(dto.restaurant_id, dto.number)
        if existing:
            raise HTTPException(status_code=409, detail="Table number already exists in this restaurant.")

        table = Table(
            id=uuid4(),
            restaurant_id=dto.restaurant_id,
            number=dto.number,
            capacity=dto.capacity,
            location=dto.location
        )

        saved = self.table_repo.save(table)
        return TableResponseDto(**saved.model_dump())

    def update_table(self, table_id: UUID, dto: UpdateTableDTO) -> TableResponseDto:
        table = self.table_repo.get_by_id(table_id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found.")

        # Si se intenta cambiar el número, validamos duplicado
        if dto.number and dto.number != table.number:
            existing = self.table_repo.get_by_restaurant_and_table_number(table.restaurant_id, dto.number)
            if existing:
                raise HTTPException(status_code=409, detail="Table number already exists in this restaurant.")

        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(table, field, value)

        updated = self.table_repo.modify(table)
        return TableResponseDto(**updated.model_dump())

    def delete_table(self, table_id: UUID) -> None:
        table = self.table_repo.get_by_id(table_id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found.")
        self.table_repo.delete(table_id)

    def get_table_by_id(self, table_id: UUID) -> TableResponseDto:
        table = self.table_repo.get_by_id(table_id)
        if not table:
            raise HTTPException(status_code=404, detail="Table not found.")
        return TableResponseDto(**table.model_dump())

    def get_tables_by_restaurant(self, restaurant_id: UUID) -> List[TableResponseDto]:
        tables = self.table_repo.get_by_restaurant_id(restaurant_id)
        return [TableResponseDto(**t.model_dump()) for t in tables]

    def get_available_tables(self, restaurant_id: UUID, capacity: int, location: str) -> List[TableResponseDto]:
        tables = self.table_repo.get_available_tables(restaurant_id, capacity, location)
        return [TableResponseDto(**t.model_dump()) for t in tables]
