from pydantic import BaseModel

class UpdateTableDTO(BaseModel):
    capacity: int
    location: str
