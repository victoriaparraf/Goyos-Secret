from typing import Optional
from pydantic import BaseModel
from datetime import time

class UpdateRestaurantDTO(BaseModel):
    name: Optional[str]
    location: Optional[str]
    opening_time: Optional[time]
    closing_time: Optional[time]