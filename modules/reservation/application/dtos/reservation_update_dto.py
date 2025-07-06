from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ReservationUpdateDto(BaseModel):
    start_time: Optional[datetime] 
    end_time: Optional[datetime] 
    num_people: Optional[int] 
    special_instructions: Optional[str]
    status: Optional[str] 
    preordered_dishes: Optional[list[UUID]] 
