from fastapi import FastAPI


app = FastAPI(
    title="Goyo´s Secrets Restaurants API",
    description="API para gestionar restaurantes, reservaciones, usuarios y menus.",
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