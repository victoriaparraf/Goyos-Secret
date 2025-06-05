from abc import ABC, abstractmethod
from typing import Optional
from modules.auth.domain.user import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su nombre de email."""
        pass

    @abstractmethod
    def create_user(self, user: User) -> User:
        """Crea un nuevo usuario en el sistema."""
        pass

    @abstractmethod
    def modify_user(self, user: User) -> User:
        """Modificar un usuario en el sistema."""
        pass

    @abstractmethod
    def get_by_id(self, user_uuid: str) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        pass