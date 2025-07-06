from pydantic import BaseModel
from uuid import UUID

class TableResponseDto(BaseModel):
    id: UUID
    restaurant_id: UUID
    number: int
    capacity: int
    location: str
