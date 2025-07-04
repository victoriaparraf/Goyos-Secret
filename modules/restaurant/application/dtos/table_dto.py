from pydantic import BaseModel
from uuid import UUID

class TableDTO(BaseModel):
    id: UUID
    restaurant_id: UUID
    table_number: int
    capacity: int
    location: str

class CreateTableDTO(BaseModel):
    restaurant_id: UUID
    table_number: int
    capacity: int
    location: str

class UpdateTableDTO(BaseModel):
    capacity: int
    location: str
