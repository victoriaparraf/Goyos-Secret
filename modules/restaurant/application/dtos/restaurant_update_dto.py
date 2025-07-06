from typing import Optional
from pydantic import BaseModel
from datetime import time

class UpdateRestaurantDTO(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None