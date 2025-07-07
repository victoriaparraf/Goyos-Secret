from uuid import UUID
from pydantic import BaseModel

from modules.auth.domain.user import UserRole

class UserRegisterDto(BaseModel):
    name: str
    email: str
    password: str
    role: UserRole