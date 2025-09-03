from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

from app.domain.enums.reservation import ReservationStatus


# The base model for a reservation, containing shared fields
class ReservationBase(BaseModel):
    user_id: UUID = Field(..., description="The ID of the user making the reservation")
    item_description: str = Field(
        ..., description="Description of the item being reserved"
    )


# A model for creating a new reservation (used for API input)
class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: UUID = Field(..., description="The unique identifier for the reservation")
    status: ReservationStatus = Field(..., description="The status of the reservation")
    created_at: datetime = Field(
        ..., description="Timestamp when the reservation was created"
    )
    update_at: datetime = Field(
        ..., description="Timestamp when the reservation was last updated"
    )

    class Config:
        from_attributes = True
