from sqlmodel import SQLModel, Field
from uuid import uuid4, UUID
from modules.auth.domain.user import User, UserRole

class UserDB(SQLModel, User, table=True):
    uuid: UUID = Field(default_factory=uuid4, index=True, primary_key=True)
    name: str
    email: str
    hashed_password: str
    role: UserRole

# Convertir de UserDB (infraestructura) a User (dominio)
def to_domain(user_db: UserDB) -> User:
    return User(
        uuid=user_db.uuid,
        name=user_db.name,
        email=user_db.email,
        hashed_password=user_db.hashed_password,
        role=user_db.role
    )

# Convertir de User (dominio) a UserDB (infraestructura)
def to_db(user: User) -> UserDB:
    return UserDB(
        name=user.name,
        email=user.email.lower(),
        hashed_password=user.hashed_password,
        role=user.role
    )