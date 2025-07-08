from fastapi import APIRouter, Depends, HTTPException, Security
from sqlmodel import Session
from modules.core.db_connection import get_db
from modules.dashboard.application.dashboard_services import DashboardService
from modules.auth.infrastructure.auth_controller import get_current_user
from modules.auth.domain.user import UserRole

router = APIRouter()

def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardService(db)

@router.get("/reservas")
def get_reservas_por_dia_y_semana(
    service: DashboardService = Depends(get_dashboard_service),
    current_user = Security(get_current_user, scopes=["admin:dashboard"])
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return service.get_reservations_summary()

@router.get("/platos")
def get_top_platos_preordenados(
    service: DashboardService = Depends(get_dashboard_service),
    current_user = Security(get_current_user, scopes=["admin:dashboard"])
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return service.get_top_preordered_dishes()

@router.get("/ocupacion")
def get_ocupacion_por_restaurante(
    service: DashboardService = Depends(get_dashboard_service),
    current_user = Security(get_current_user, scopes=["admin:dashboard"])
):
    try:
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Unauthorized")
        return service.get_occupancy_percentage()
    except Exception as e:
        # Aquí verás el mensaje de error real
        raise HTTPException(status_code=500, detail=f"Dashboard error: {e}")