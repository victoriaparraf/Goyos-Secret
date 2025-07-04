from pydantic import BaseModel
from datetime import time
from uuid import UUID

class RestaurantDTO(BaseModel):
    id: UUID
    name: str
    location: str
    opening_time: time
    closing_time: time

class CreateRestaurantDTO(BaseModel):
    name: str
    location: str
    opening_time: time
    closing_time: time

class UpdateRestaurantDTO(BaseModel):
    name: str
    location: str
    opening_time: time
    closing_time: time
