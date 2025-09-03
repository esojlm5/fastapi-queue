from fastapi import FastAPI
from app.presentation.http.controllers.reservation import router as reservation

app = FastAPI()

app.include_router(reservation, prefix="/reservations", tags=["reservations"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
