from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from datetime import Time


class MenuItem(BaseModel):
    uuid: UUID
    name: str
    description: str
    category: str
    available_stock: int
    image_url: Optional[str]
