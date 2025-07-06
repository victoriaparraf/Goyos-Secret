from fastapi import APIRouter, Depends, HTTPException, Security, status
from sqlmodel import Session
from typing import List
from uuid import UUID
from modules.auth.domain.user import UserRole
from modules.auth.infrastructure.auth_controller import get_current_user
from modules.core.db_connection import get_db
from modules.restaurant.infrastructure.restaurant_repository import RestaurantRepository
from modules.restaurant.infrastructure.table_repository import TableRepository
from modules.restaurant.application.restaurant_services import RestaurantService
from modules.restaurant.application.dtos.restaurant_create_dto import RestaurantCreateDto
from modules.restaurant.application.dtos.restaurant_update_dto import RestaurantUpdateDto
from modules.restaurant.application.dtos.restaurant_response_dto import RestaurantResponseDto

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

# Dependency to inject the service
def get_restaurant_service(db: Session = Depends(get_db)) -> RestaurantService:
    restaurant_repo = RestaurantRepository(db)
    table_repo = TableRepository(db)
    return RestaurantService(restaurant_repo, table_repo)

# GET: List all restaurants (open to all)
@router.get("/", response_model=List[RestaurantResponseDto])
def list_restaurants(service: RestaurantService = Depends(get_restaurant_service)):
    return service.list_restaurants()

# GET: Get restaurant by ID (open to all)
@router.get("/{restaurant_id}", response_model=RestaurantResponseDto)
def get_restaurant(
    restaurant_id: UUID,
    service: RestaurantService = Depends(get_restaurant_service)
):
    return service.get_restaurant_by_id(restaurant_id)

# POST: Create restaurant (admin only)
@router.post("/", response_model=RestaurantResponseDto, status_code=status.HTTP_201_CREATED)
def create_restaurant(
    dto: RestaurantCreateDto,
    service: RestaurantService = Depends(get_restaurant_service),
    current_user = Security(get_current_user, scopes=["admin:restaurants"])
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can create restaurants.")
    return service.create_restaurant(dto)

# PUT: Modify restaurant (admin only)
@router.put("/{restaurant_id}", response_model=RestaurantResponseDto)
def update_restaurant(
    restaurant_id: UUID,
    dto: RestaurantUpdateDto,
    service: RestaurantService = Depends(get_restaurant_service),
    current_user = Security(get_current_user, scopes=["admin:restaurants"])
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can modify restaurants.")
    return service.update_restaurant(restaurant_id, dto)

# DELETE: Delete restaurant (admin only)
@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    restaurant_id: UUID,
    service: RestaurantService = Depends(get_restaurant_service),
    current_user = Security(get_current_user, scopes=["admin:restaurants"])
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can delete restaurants.")
    service.delete_restaurant(restaurant_id)
    return
