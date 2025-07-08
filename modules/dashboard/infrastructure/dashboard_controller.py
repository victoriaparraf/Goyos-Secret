from fastapi import APIRouter, Depends, Security, HTTPException, status, Query
from typing import List, Dict, Any
from datetime import datetime, date, timedelta
from sqlmodel import Session
from modules.core.db_connection import get_db
from modules.auth.infrastructure.auth_controller import get_current_user
from modules.auth.domain.user import UserRole
from modules.reservation.infrastructure.reservation_repository import ReservationRepository
from modules.menu.infrastructure.menu_repository import MenuRepository
from modules.restaurant.infrastructure.table_repository import TableRepository
from modules.restaurant.infrastructure.restaurant_repository import RestaurantRepository
from modules.dashboard.application.dashboard_services import DashboardService

router = APIRouter()

def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    reservation_repo = ReservationRepository(db)
    menu_repo = MenuRepository(db)
    table_repo = TableRepository(db)
    restaurant_repo = RestaurantRepository(db)
    return DashboardService(reservation_repo, menu_repo, table_repo, restaurant_repo)

@router.get("/reservas", response_model=Dict[date, int])
def get_total_reservations(
    start_date: date = Query(..., description="Start date for reservation count (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date for reservation count (YYYY-MM-DD)"),
    service: DashboardService = Depends(get_dashboard_service),
    current_user = Security(get_current_user, scopes=["admin:dashboard"])
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can access this data.")
    return service.get_total_reservations_by_date_range(start_date, end_date)

@router.get("/platos", response_model=List[Dict[str, Any]])
def get_top_preordered_dishes(
    limit: int = Query(5, ge=1, description="Number of top dishes to return"),
    service: DashboardService = Depends(get_dashboard_service),
    current_user = Security(get_current_user, scopes=["admin:dashboard"])
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can access this data.")
    return service.get_top_preordered_dishes(limit)

@router.get("/ocupacion", response_model=Dict[str, float])
def get_occupancy_percentage(
    restaurant_id: str = Query(..., description="UUID of the restaurant"),
    service: DashboardService = Depends(get_dashboard_service),
    current_user = Security(get_current_user, scopes=["admin:dashboard"])
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can access this data.")
    return service.get_occupancy_percentage(restaurant_id)
