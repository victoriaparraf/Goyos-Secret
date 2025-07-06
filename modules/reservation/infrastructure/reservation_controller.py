from fastapi import APIRouter, Depends, HTTPException, Security, status, Query
from fastapi.security import SecurityScopes
from typing import List
from uuid import UUID
from datetime import datetime
from sqlmodel import Session
from modules.core.db_connection import get_db
from modules.auth.infrastructure.auth_controller import get_current_user
from modules.auth.domain.user import UserRole
from modules.reservation.application.reservation_services import ReservationService
from modules.reservation.infrastructure.reservation_repository import ReservationRepository
from modules.restaurant.infrastructure.table_repository import TableRepository
from modules.menu.infrastructure.menu_repository import MenuRepository
from modules.reservation.application.dtos.reservation_create_dto import ReservationCreateDto
from modules.reservation.application.dtos.reservation_response_dto import ReservationResponseDto

router = APIRouter()

# Dependency injection
def get_reservation_service(db: Session = Depends(get_db)) -> ReservationService:
    reservation_repo = ReservationRepository(db)
    table_repo = TableRepository(db)
    menu_repo = MenuRepository(db)
    return ReservationService(reservation_repo, table_repo, menu_repo)

# POST /reservations/
@router.post("/", response_model=ReservationResponseDto, status_code=status.HTTP_201_CREATED)
def create_reservation(
    dto: ReservationCreateDto,
    service: ReservationService = Depends(get_reservation_service),
    current_user = Security(get_current_user, scopes=["reservation:write"])
):
    return service.create_reservation(current_user.uuid, dto)

# GET /reservations/
@router.get("/", response_model=List[ReservationResponseDto])
def list_user_reservations(
    service: ReservationService = Depends(get_reservation_service),
    current_user = Security(get_current_user, scopes=["reservation:read"])
):
    return service.get_reservations_by_user(current_user.uuid)

# GET /reservations/{id}
@router.get("/{reservation_id}", response_model=ReservationResponseDto)
def get_reservation_by_id(
    reservation_id: UUID,
    service: ReservationService = Depends(get_reservation_service),
    current_user = Security(get_current_user, scopes=["reservation:read", "admin:reservations"])
):
    reservation = service.get_reservation_by_id(reservation_id)
    if current_user.role == UserRole.CLIENT and reservation.user_id != current_user.uuid:
        raise HTTPException(status_code=403, detail="You can only access your own reservations.")
    return reservation

# DELETE /reservations/{id}
@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_reservation(
    reservation_id: UUID,
    service: ReservationService = Depends(get_reservation_service),
    current_user = Security(get_current_user, scopes=["reservation:write", "admin:reservations"])
):
    is_admin = current_user.role == UserRole.ADMIN
    service.cancel_reservation(reservation_id, current_user.uuid, is_admin)
    return

# GET /reservations/restaurant/{restaurant_id}
@router.get("/restaurant/{restaurant_id}", response_model=List[ReservationResponseDto])
def get_reservations_by_restaurant(
    restaurant_id: UUID,
    service: ReservationService = Depends(get_reservation_service),
    current_user = Security(get_current_user, scopes=["admin:reservations"])
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can access this data.")
    return service.get_all_by_restaurant(restaurant_id)

# GET /reservations/range?start=...&end=...
@router.get("/range", response_model=List[ReservationResponseDto])
def get_reservations_by_date_range(
    start: datetime = Query(...),
    end: datetime = Query(...),
    service: ReservationService = Depends(get_reservation_service),
    current_user = Security(get_current_user, scopes=["admin:reservations"])
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only admins can access this data.")
    return service.get_by_date_range(start, end)
