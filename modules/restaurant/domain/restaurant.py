from pydantic import BaseModel
from uuid import UUID
from datetime import time

class Restaurant(BaseModel):
    id: UUID
    name: str
    address: str
    opening_time: time
    closing_time: time
