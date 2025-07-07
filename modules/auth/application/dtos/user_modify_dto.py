from pydantic import BaseModel
from typing import Optional

from modules.auth.domain.user import UserRole

class UserModifyDto(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None