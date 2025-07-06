from pydantic import BaseModel
from uuid import UUID

class CreateTableDTO(BaseModel):
    restaurant_id: UUID
    table_number: int
    capacity: int
    location: str