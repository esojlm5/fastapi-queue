from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from starlette.exceptions import HTTPException
from app.presentation.http.controllers.reservation import router as reservation
from app.core.config import settings

security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    print("Verifying token...", credentials.credentials)
    token = credentials.credentials
    if str(token) != str(settings.API_TOKEN):
        raise HTTPException(status_code=403, detail="Invalid or missing token")


app = FastAPI(dependencies=[Depends(verify_token)])

app.include_router(reservation, prefix="/reservations", tags=["reservations"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
