from pydantic import BaseModel
from uuid import UUID

class Table(BaseModel):
    id: UUID
    restaurant_id: UUID
    number: int
    capacity: int
    location: str

