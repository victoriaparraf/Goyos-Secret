from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class ReservationStatus(Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class Reservation(BaseModel):
    uuid: UUID
    user_id: UUID
    table_id: UUID
    start_time: datetime
    end_time: datetime
    num_people: int
    special_instructions: Optional[str]
    preordered_dishes: Optional[List[UUID]] = []  # <<<< AÑADIDO
    status: ReservationStatus
