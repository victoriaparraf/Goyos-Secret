from uuid import UUID
from typing import List
from pydantic import BaseModel
from modules.menu.domain import PreOrderItem


class Reservation(BaseModel):
    uuid: UUID
    pre_orders: List[PreOrderItem] = []