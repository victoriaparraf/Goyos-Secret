from enum import Enum
from pydantic import BaseModel
from uuid import UUID

ROLE_SCOPES = {
    "admin": [
        "admin:all", "admin:restaurants", "admin:menu", "admin:reservations", "admin:dashboard"
    ],
    "client": [
        "client:read", "client:write"
    ]
}

class UserRole(Enum):
    ADMIN = "admin"
    CLIENT = "client"

class User(BaseModel):
    uuid: UUID
    name: str
    email: str
    hashed_password: str
    role: UserRole
