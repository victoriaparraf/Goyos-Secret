from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from modules.reservation.domain.reservation import ReservationStatus

class ReservationResponseDto(BaseModel):
    uuid: UUID
    user_id: UUID
    table_id: UUID
    start_time: datetime
    end_time: datetime
    num_people: int
    special_instructions: Optional[str] = None
    status: ReservationStatus
    preordered_dishes: Optional[List[UUID]] = []
    restaurant_name: str
