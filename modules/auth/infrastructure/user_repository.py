from typing import Optional
from uuid import UUID

from sqlmodel import Session, select
from modules.auth.domain.user import User
from modules.auth.infrastructure.user_db_model import UserDB
from modules.auth.domain.user_repository_interface import UserRepositoryInterface

class UserRepository(UserRepositoryInterface):
    
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(UserDB).where(UserDB.email == email)
        result = self.db.exec(statement).first()
        return result

    def create_user(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def modify_user(self, user: UserDB) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_uuid: str) -> Optional[UserDB]:
        statement = select(UserDB).where(UserDB.uuid == user_uuid)
        result = self.db.exec(statement).first()
        return result
    