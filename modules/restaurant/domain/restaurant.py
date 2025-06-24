from uuid import UUID
from pydantic import BaseModel
from datetime import Time


class Restaurant(BaseModel):
    uuid: UUID
    name: str
    opening_time: Time
    closing_time: Time
    location: str