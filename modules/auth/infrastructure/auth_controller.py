from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from sqlmodel import Session
from passlib.context import CryptContext
from modules.auth.application.dtos.user_login_dto import UserLoginDto
from modules.auth.application.dtos.user_modify_dto import UserModifyDto
from modules.auth.application.dtos.user_register_dto import UserRegisterDto
from modules.auth.infrastructure.user_db_model import UserDB, to_db
from modules.core.db_connection import get_db
from modules.auth.infrastructure.user_repository import UserRepository
from modules.auth.application.user_services import UserServices
from modules.auth.application.auth_services import AuthServices
from modules.auth.domain.user import UserRole, ROLE_SCOPES

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

pwd_context = CryptContext(schemes=["bcrypt"])

def get_user_services(db: Session = Depends(get_db)) -> UserServices:
    repository = UserRepository(db)
    return UserServices(repository)

def get_auth_services(db: Session = Depends(get_db)) -> AuthServices:
    repository = UserRepository(db)
    return AuthServices(repository)

def get_current_user(
        security_scopes: SecurityScopes,
        token: str = Depends(oauth2_scheme),
        user_service: UserServices = Depends(get_user_services),
        auth_service: AuthServices = Depends(get_auth_services)
    ):
    current_user = auth_service.get_current_user(token, security_scopes.scopes)
    if not current_user:
        raise HTTPException(status_code=401, detail="Error token")
    user = user_service.get_user_by_id(current_user.uuid)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthServices = Depends(get_auth_services)
):
    try:
        user = auth_service.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=403, detail="Error: Incorrect email or password")
        scopes = ROLE_SCOPES.get(user.role.value, [])
        token = auth_service.create_access_token(data={"sub": str(user.uuid)}, scopes=scopes)
        return {
            "access_token": token, 
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.post("/register")
async def register_user(
    user_data: UserRegisterDto,
    service: UserServices = Depends(get_user_services)
):
    try: 
        user_db = to_db(user_data)
        user_db.hashed_password = pwd_context.hash(user_db.hashed_password)
        created_user = service.create_user(user_db)
        return {
            "message": "User registered successfully", 
            "user": created_user
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
@router.put("/modify/{user_id}")
async def modify_user(
    user_id: str,
    user_data: UserModifyDto,
    service: UserServices = Depends(get_user_services),
    current_user = Security(get_current_user, scopes=["admin:all", "client:write"])
):
    # Solo admin puede modificar cualquier usuario
    # Cliente solo puede modificar su propio usuario
    if (
        current_user.role.value == "client"
        and str(current_user.uuid) != user_id
    ):
        raise HTTPException(status_code=403, detail="You can only modify your own user.")
    try:
        user = service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data.hashed_password = pwd_context.hash(user_data.hashed_password)
        updated_user = service.modify_user(current_user=user, modified_user=user_data)
        return {
            "message": "User modified successfully", 
            "user": updated_user
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
