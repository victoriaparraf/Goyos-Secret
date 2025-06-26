from uuid import UUID
from pydantic import BaseModel
from typing import Optional

class PreOrderItem(BaseModel):
    id: UUID
    menu_item_id: UUID
    reservation_id: UUID
    quantity: int
    special_instructions: Optional[str] = None