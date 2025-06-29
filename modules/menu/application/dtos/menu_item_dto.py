from pydantic import BaseModel
from typing import Optional


class MenuItemModifyDto(BaseModel):
    name: str
    description: str
    category: str
    price: float
    available_stock: int
    image_url: Optional[str]


class MenuItemRegisterDto(BaseModel):
    name: str
    description: str
    category: str
    price: float
    available_stock: int
    image_url: Optional[str]
