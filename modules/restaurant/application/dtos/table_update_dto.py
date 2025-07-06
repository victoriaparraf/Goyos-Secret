from pydantic import BaseModel
from typing import Optional

class UpdateTableDTO(BaseModel):
    number: Optional[int]
    capacity: Optional[int]
    location: Optional[str]
