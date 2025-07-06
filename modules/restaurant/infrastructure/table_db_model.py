from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from modules.restaurant.domain.table import Table

class TableDBModel(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    restaurant_id: UUID = Field(foreign_key="restaurantdbmodel.id", index=True)
    number: int
    capacity: int
    location: str

def to_domain(table_db: TableDBModel) -> Table:
    return Table(
        id=table_db.id,
        restaurant_id=table_db.restaurant_id,
        number=table_db.number,
        capacity=table_db.capacity,
        location=table_db.location
    )

def to_db(table: Table) -> TableDBModel:
    return TableDBModel(
        id=table.id,
        restaurant_id=table.restaurant_id,
        number=table.number,
        capacity=table.capacity,
        location=table.location
    )
