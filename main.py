from fastapi import FastAPI
from sqlmodel import SQLModel
from modules.core.db_connection import engine
from modules.auth.infrastructure.auth_controller import router as auth_router
from modules.menu.infrastructure.menu_controller import router as menu_router
from modules.restaurant.infrastructure.restaurant_controller import router as restaurant_router
from modules.reservation.infrastructure.reservation_controller import router as reservation_router

SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="Goyo´s Secrets Restaurants API",
    description="API para gestionar restaurantes, reservaciones, usuarios y menús.",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/test", tags=["API Test"])
async def test_db():
    try:
        return {"message": "API corriendo correctamente"}
    except Exception as e:
        return {"error": str(e)}

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(menu_router, prefix="/menu", tags=["Menu"])
app.include_router(restaurant_router, prefix="/restaurants", tags=["Restaurant"])
app.include_router(reservation_router, prefix="/reservations", tags=["Reservation"])
