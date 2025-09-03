from uuid import UUID
from traceback import print_exc
from supabase import create_client, Client

from app.domain.entities.reservation import Reservation, ReservationCreate
from app.domain.ports.reservation.abstract import AbstractReservationRepository


class ReservationRepoError(Exception):
    pass


class SupabaseReservationRepository(AbstractReservationRepository):
    def __init__(self, supbase_url: str, supabase_key: str):
        self.client: Client = create_client(supbase_url, supabase_key)

    def create_table_if_not_exists(self) -> None:
        pass

    async def count_reservations(self) -> int:
        try:
            response = (
                self.client.table("reservations")
                .select("*", count="exact", head=True)
                .execute()
            )

            return response.count if response.count is not None else 50
        except Exception as e:
            print("Error counting reservations:", e)
            print_exc()
            return 0

    async def create_reservation(self, reservation: ReservationCreate) -> Reservation:
        try:
            response = (
                self.client.table("reservations")
                .insert(reservation.model_dump(mode="json"))
                .execute()
            )
            data = response.data[0]
            return Reservation(**data)
        except Exception as e:
            print("Error inserting reservation:", e)
            print_exc()
            raise

    async def get_reservation_by_id(self, reservation_id: UUID) -> Reservation | None:
        print("reservationnn", reservation_id)
        try:
            response = (
                self.client.table("reservations")
                .select("*")
                .eq("id", str(reservation_id))
                .execute()
            )
            data = response.data
            if data:
                return Reservation(**data[0])
            return None
        except Exception as e:
            print("Error fetching reservation by ID:", e)
            print_exc()
            raise ReservationRepoError("Error fetching reservation by ID")

    async def list_reservations(self) -> list[Reservation]:
        response = self.client.table("reservations").select("*").execute()
        return [Reservation(**item) for item in response.data]
