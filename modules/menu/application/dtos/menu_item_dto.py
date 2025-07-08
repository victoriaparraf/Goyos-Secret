
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class MenuItemModifyDto(BaseModel):
    name: Optional[str] = None 
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    available_stock: Optional[int] = None
    image_url: Optional[str] = None


class MenuItemRegisterDto(BaseModel):
    name: str
    description: str
    category: str
    price: float
    available_stock: int
    restaurant_id: UUID
    image_url: Optional[str] = None # Optional, can be set later if needed
