from typing import Optional
from uuid import UUID, uuid4
from fastapi import HTTPException
from passlib.context import CryptContext
from modules.auth.application.dtos.user_modify_dto import UserModifyDto
from modules.auth.application.dtos.user_register_dto import UserRegisterDto
from modules.auth.domain.user import User, UserRole
from modules.auth.domain.user_repository_interface import UserRepositoryInterface

pwd_context = CryptContext(schemes=["bcrypt"])

class UserServices:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo
    
    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        return self.user_repo.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su email."""
        return self.user_repo.get_by_email(email.lower)
    
    def create_user(self, user: User) -> User:
        """Crea un nuevo usuario en el sistema."""
        user.email = user.email.lower

        if user.role == UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Error: Inadmisible role admin")
        
        result = self.get_user_by_email(user.email)
        if result:
            raise HTTPException(status_code=409, detail="Error: Email already registered")
        
        return self.user_repo.create_user(user)
    
    def modify_user(self, current_user: User, modified_user: UserModifyDto) -> User: 
        """Modifica un usuario en el sistema."""
        for field, value in modified_user.model_dump().items():
            setattr(current_user, field, value)

        return self.user_repo.modify_user(current_user)