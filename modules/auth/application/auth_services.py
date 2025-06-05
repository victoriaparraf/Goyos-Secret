from datetime import datetime, timedelta
from typing import Optional, List
from uuid import UUID

from fastapi import HTTPException
import jwt  # pyjwt
from passlib.context import CryptContext

from modules.auth.domain.user import User
from modules.auth.domain.user_repository_interface import UserRepositoryInterface

# Configuración JWT
SECRET_KEY = "ApIlAdOrEs20"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthServices:
    def __init__(self, user_repo: UserRepositoryInterface):
        self.user_repo = user_repo

    # Caso de uso: Autenticar usuario
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        if not pwd_context.verify(password, user.hashed_password):
            return None
        return user

    # Caso de uso: Crear token de acceso JWT
    def create_access_token(self, data: dict, scopes: List[str], expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        to_encode.update({"scopes": scopes})
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        if isinstance(encoded_jwt, bytes):
            encoded_jwt = encoded_jwt.decode("utf-8")
        return encoded_jwt

    # Caso de uso: Obtener usuario actual a partir del token
    def get_current_user(self, token: str, required_scopes: List[str]) -> Optional[User]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            uuid: str = payload.get("sub")
            token_scopes: List[str] = payload.get("scopes", [])
            if uuid is None:
                return None
            if not any(scope in token_scopes for scope in required_scopes):
                raise HTTPException(status_code=403, detail="You dont have access to this endpoint")
            user = self.user_repo.get_by_id(uuid)
            return user
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Expired token")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token error")