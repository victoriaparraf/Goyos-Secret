from enum import Enum
from pydantic import BaseModel, EmailStr
from uuid import UUID

ROLE_SCOPES = {
    "admin": [
        "admin:all", "admin:restaurants", "admin:menu", "admin:reservation", "admin:dashboard"
    ],
    "client": [
        "client:read", "client:write", "menu:read", "reservation:read", "reservation:write", "restaurants:read"
    ]
}

class UserRole(Enum):
    ADMIN = "admin"
    CLIENT = "client"

class User(BaseModel):
    uuid: UUID
    name: str
    email: EmailStr
    hashed_password: str
    role: UserRole