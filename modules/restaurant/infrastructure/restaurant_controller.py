from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from modules.core.db_connection import get_db
from modules.restaurant.application.restaurant_services import RestaurantServices
from modules.restaurant.application.table_services import TableServices
from modules.restaurant.infrastructure.restaurant_repository import RestaurantRepository
from modules.restaurant.infrastructure.table_repository import TableRepository
from modules.restaurant.application.dtos.restaurant_dto import CreateRestaurantDTO, UpdateRestaurantDTO, RestaurantDTO
from modules.restaurant.application.dtos.table_dto import CreateTableDTO, TableDTO
from modules.auth.application.auth_services import get_current_user, User # Asumiendo que existe
from modules.restaurant.domain.exceptions import (
    RestaurantAlreadyExistsError,
    RestaurantNotFoundError,
    TableNumberConflictError,
    CannotDeleteRestaurantWithTablesError,
)

router = APIRouter()

def get_restaurant_services(db: Session = Depends(get_db)) -> RestaurantServices:
    return RestaurantServices(RestaurantRepository(db), TableRepository(db))

def get_table_services(db: Session = Depends(get_db)) -> TableServices:
    return TableServices(TableRepository(db))

@router.post("/restaurants/", response_model=RestaurantDTO)
def create_restaurant(
    restaurant_dto: CreateRestaurantDTO,
    restaurant_services: RestaurantServices = Depends(get_restaurant_services),
    current_user: User = Depends(get_current_user)
):
    try:
        return restaurant_services.create_restaurant(restaurant_dto, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except RestaurantAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/restaurants/{restaurant_id}", response_model=RestaurantDTO)
def update_restaurant(
    restaurant_id: UUID,
    restaurant_dto: UpdateRestaurantDTO,
    restaurant_services: RestaurantServices = Depends(get_restaurant_services),
    current_user: User = Depends(get_current_user)
):
    try:
        return restaurant_services.update_restaurant(restaurant_id, restaurant_dto, current_user)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except RestaurantNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/restaurants/{restaurant_id}")
def delete_restaurant(
    restaurant_id: UUID,
    restaurant_services: RestaurantServices = Depends(get_restaurant_services),
    current_user: User = Depends(get_current_user)
):
    try:
        restaurant_services.delete_restaurant(restaurant_id, current_user)
        return {"message": "Restaurante eliminado correctamente."}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except CannotDeleteRestaurantWithTablesError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.post("/tables/", response_model=TableDTO)
def create_table(
    table_dto: CreateTableDTO,
    table_services: TableServices = Depends(get_table_services)
):
    try:
        return table_services.create_table(table_dto)
    except TableNumberConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/restaurants/{restaurant_id}/tables/available")
def get_available_tables(
    restaurant_id: UUID,
    capacity: int,
    location: str,
    table_services: TableServices = Depends(get_table_services)
):
    return table_services.get_available_tables(restaurant_id, capacity, location)
