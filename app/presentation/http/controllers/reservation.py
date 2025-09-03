from typing import Annotated
from fastapi import HTTPException
from uuid import UUID
from fastapi import APIRouter
from fastapi.params import Depends
from app.core.config import settings
from app.domain.entities.reservation import Reservation, ReservationCreate
from app.infrastructure.adapters.reservation.supabase_repo import (
    SupabaseReservationRepository,
)


def get_repo():
    return SupabaseReservationRepository(settings.SUPABASE_URL, settings.SUPABASE_KEY)


router = APIRouter()


@router.post("/checkout", response_model=ReservationCreate)
async def checkout(
    reservation_data: ReservationCreate,
    repo: Annotated[SupabaseReservationRepository, Depends(get_repo)],
):
    # repo = SupabaseReservationRepository(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    MAX_RESERVATIONS = 50
    current_count = await repo.count_reservations()

    if current_count >= MAX_RESERVATIONS:
        return {"error": "Maximum number of reservations reached."}
    else:
        print("repooooooo", current_count)
        print("reservation data", reservation_data)
        reservation = await repo.create_reservation(reservation_data)
        print("reservation result", reservation)
        return reservation


@router.get("/checkout/{reservation_id}", response_model=Reservation)
async def read_item(
    reservation_id: UUID,
    repo: Annotated[SupabaseReservationRepository, Depends(get_repo)],
    q: str | None = None,
):
    # repo = SupabaseReservationRepository(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    try:
        reservation = await repo.get_reservation_by_id(reservation_id)
        if reservation is None:
            return {"error": "Reservation not found."}
        return reservation
    except Exception as e:
        HTTPException(status_code=500, detail=str(e))
