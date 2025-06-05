from uuid import UUID
from pydantic import BaseModel

from modules.auth.domain.user import UserRole

class UserRegisterDto(BaseModel):
    name: str
    email: str
    hashed_password: str
    role: UserRole
