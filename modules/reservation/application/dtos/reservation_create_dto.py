from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional

class ReservationCreateDto(BaseModel):
    table_id: UUID
    start_time: datetime
    end_time: datetime
    num_people: int 
    special_instructions: Optional[str]
    preordered_dishes: Optional[list[UUID]] 

