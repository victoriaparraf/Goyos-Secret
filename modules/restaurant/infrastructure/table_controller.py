from fastapi import APIRouter, Depends, HTTPException, Security, status
from typing import List
from uuid import UUID
from sqlmodel import Session
from modules.core.db_connection import get_db
from modules.auth.infrastructure.auth_controller import get_current_user
from modules.auth.domain.user import UserRole
from modules.restaurant.application.table_services import TableService
from modules.restaurant.infrastructure.table_repository import TableRepository
from modules.restaurant.application.dtos.table_create_dto import TableCreateDto
from modules.restaurant.application.dtos.table_update_dto import TableUpdateDto
from modules.restaurant.application.dtos.table_response_dto import TableResponseDto

router = APIRouter(prefix="/tables", tags=["Tables"])

# Dependency injection
def get_table_service(db: Session = Depends(get_db)) -> TableService:
    repo = TableRepository(db)
    return TableService(repo)

# GET /tables/{id}
@router.get("/{table_id}", response_model=TableResponseDto)
def get_table_by_id(
    table_id: UUID,
    service: TableService = Depends(get_table_service),
    current_user = Security(get_current_user, scopes=["admin:restaurants", "restaurant:read"]),
):
    return service.get_table_by_id(table_id)

# GET /tables/restaurant/{restaurant_id}
@router.get("/restaurant/{restaurant_id}", response_model=List[TableResponseDto])
def get_tables_by_restaurant(
    restaurant_id: UUID,
    service: TableService = Depends(get_table_service),
    current_user = Security(get_current_user, scopes=["admin:restaurants", "restaurant:read"]),
):
    return service.get_tables_by_restaurant(restaurant_id)

# GET /tables/available
@router.get("/available/search", response_model=List[TableResponseDto])
def search_available_tables(
    restaurant_id: UUID,
    capacity: int,
    location: str,
    service: TableService = Depends(get_table_service),
    current_user = Security(get_current_user, scopes=["admin:restaurants", "restaurant:read"]),
):
    return service.get_available_tables(restaurant_id, capacity, location)

# POST /tables/
@router.post("/", response_model=TableResponseDto, status_code=status.HTTP_201_CREATED)
def create_table(
    dto: TableCreateDto,
    service: TableService = Depends(get_table_service),
    current_user = Security(get_current_user, scopes=["admin:restaurants"])
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can create tables.")
    return service.create_table(dto)

# PUT /tables/{id}
@router.put("/{table_id}", response_model=TableResponseDto)
def update_table(
    table_id: UUID,
    dto: TableUpdateDto,
    service: TableService = Depends(get_table_service),
    current_user = Security(get_current_user, scopes=["admin:restaurants"])
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can update tables.")
    return service.update_table(table_id, dto)

# DELETE /tables/{id}
@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(
    table_id: UUID,
    service: TableService = Depends(get_table_service),
    current_user = Security(get_current_user, scopes=["admin:restaurants"])
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can delete tables.")
    service.delete_table(table_id)
    return
