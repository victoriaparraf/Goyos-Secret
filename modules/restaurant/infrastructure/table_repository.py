from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from modules.restaurant.domain.table import Table
from modules.restaurant.domain.table_repository_interface import ITableRepository
from modules.restaurant.infrastructure.table_db_model import TableDBModel

class TableRepository(ITableRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, table_id: UUID) -> Optional[Table]:
        table_db = self.session.query(TableDBModel).filter_by(id=table_id).first()
        return Table.model_validate(table_db) if table_db else None

    def get_by_restaurant_id(self, restaurant_id: UUID) -> List[Table]:
        tables_db = self.session.query(TableDBModel).filter_by(restaurant_id=restaurant_id).all()
        return [Table.model_validate(table) for table in tables_db]

    def get_by_restaurant_and_table_number(self, restaurant_id: UUID, table_number: int) -> Optional[Table]:
        table_db = self.session.query(TableDBModel).filter_by(restaurant_id=restaurant_id, table_number=table_number).first()
        return Table.model_validate(table_db) if table_db else None

    def save(self, table: Table) -> None:
        table_db = self.session.query(TableDBModel).filter_by(id=table.id).first()
        if table_db:
            table_db.capacity = table.capacity
            table_db.location = table.location
        else:
            table_db = TableDBModel(**table.model_dump())
            self.session.add(table_db)
        self.session.commit()

    def delete(self, table_id: UUID) -> None:
        table_db = self.session.query(TableDBModel).filter_by(id=table_id).first()
        if table_db:
            self.session.delete(table_db)
            self.session.commit()

    def get_available_tables(self, restaurant_id: UUID, capacity: int, location: str) -> List[Table]:
        tables_db = self.session.query(TableDBModel).filter(
            TableDBModel.restaurant_id == restaurant_id,
            TableDBModel.capacity >= capacity,
            TableDBModel.location == location
        ).all()
        return [Table.model_validate(table) for table in tables_db]
