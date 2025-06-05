from pydantic import BaseModel

from modules.auth.domain.user import UserRole

class UserModifyDto(BaseModel):
    name: str
    email: str
    hashed_password: str