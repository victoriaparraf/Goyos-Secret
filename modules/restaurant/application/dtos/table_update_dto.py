from pydantic import BaseModel
from typing import Optional

class UpdateTableDTO(BaseModel):
    number: Optional[int] = None
    capacity: Optional[int] = None
    location: Optional[str] = None
