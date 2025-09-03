from abc import ABC, abstractmethod
from uuid import UUID


from app.domain.entities.reservation import Reservation, ReservationCreate


class AbstractReservationRepository(ABC):
    @abstractmethod
    async def create_reservation(self, reservation: ReservationCreate) -> Reservation:
        """Create a new reservation in the database."""
        pass

    @abstractmethod
    async def get_reservation_by_id(self, reservation_id: UUID) -> Reservation | None:
        """Retrieve a reservation by its ID."""
        pass

    @abstractmethod
    async def list_reservations(self) -> list[Reservation]:
        """List all reservations in the database."""
        pass
