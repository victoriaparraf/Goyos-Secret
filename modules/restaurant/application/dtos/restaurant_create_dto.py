from pydantic import BaseModel
from datetime import time

class CreateRestaurantDTO(BaseModel):
    name: str
    address: str
    opening_time: time
    closing_time: time