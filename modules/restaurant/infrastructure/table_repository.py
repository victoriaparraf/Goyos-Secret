from sqlmodel import Session, select
from typing import Optional, List
from uuid import UUID
from modules.restaurant.domain.table_repository_interface import ITableRepository
from modules.restaurant.domain.table import Table
from modules.restaurant.infrastructure.table_db_model import TableDBModel, to_domain, to_db

class TableRepository(ITableRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, table_id: UUID) -> Optional[Table]:
        result = self.db.get(TableDBModel, table_id)
        return to_domain(result) if result else None

    def get_by_restaurant_id(self, restaurant_id: UUID) -> List[Table]:
        statement = select(TableDBModel).where(TableDBModel.restaurant_id == restaurant_id)
        result = self.db.exec(statement).all()
        return [to_domain(t) for t in result]

    def get_by_restaurant_and_table_number(self, restaurant_id: UUID, table_number: int) -> Optional[Table]:
        statement = select(TableDBModel).where(
            (TableDBModel.restaurant_id == restaurant_id) &
            (TableDBModel.number == table_number)
        )
        result = self.db.exec(statement).first()
        return to_domain(result) if result else None

    def save(self, table: Table) -> Table:
        db_table = to_db(table)
        self.db.add(db_table)
        self.db.commit()
        self.db.refresh(db_table)
        return to_domain(db_table)

    def modify(self, table: Table) -> Table:
        db_table = self.db.get(TableDBModel, table.id)
        if not db_table:
            raise Exception("Table not found")

        updated = to_db(table)
        for field, value in updated.model_dump().items():
            setattr(db_table, field, value)

        self.db.add(db_table)
        self.db.commit()
        self.db.refresh(db_table)
        return to_domain(db_table)

    def delete(self, table_id: UUID) -> None:
        db_table = self.db.get(TableDBModel, table_id)
        if db_table:
            self.db.delete(db_table)
            self.db.commit()

    def get_available_tables(self, restaurant_id: UUID, capacity: int, location: str) -> List[Table]:
        statement = select(TableDBModel).where(
            (TableDBModel.restaurant_id == restaurant_id) &
            (TableDBModel.capacity >= capacity) &
            (TableDBModel.location == location)
        )
        result = self.db.exec(statement).all()
        return [to_domain(t) for t in result]
