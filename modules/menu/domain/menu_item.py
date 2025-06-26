from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class MenuItem(BaseModel):
    id: UUID
    name: str
    description: str
    category: str
    price: float
    available_stock: int
    image_url: Optional[str]
