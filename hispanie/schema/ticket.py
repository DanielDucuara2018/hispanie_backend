from pydantic import BaseModel, ConfigDict, Field

from ..model import Currency
from ..typing import CustomDateTime


class TicketCreateRequest(BaseModel):
    """Schema for creating a new ticket."""

    name: str = Field(..., min_length=1, max_length=500, description="Unique name of the ticket.")
    cost: float = Field(..., ge=0.0, description="Cost of the ticket")
    currency: Currency = Field(..., description="Currency of the ticket.", examples=["EUR"])
    event_id: str | None = Field(default=None, pattern=r"^event-[0-9a-f]{32}$")
    description: str | None = Field(None, max_length=500)


class TicketUpdateRequest(BaseModel):
    """Schema for updating a ticket."""

    id: str | None = Field(None, pattern=r"^ticket-[0-9a-f]{32}$")
    name: str | None = Field(
        None, min_length=1, max_length=500, description="Update name of the ticket."
    )
    cost: float | None = Field(None, ge=0.0, description="Update cost of the ticket")
    currency: Currency | None = Field(
        None, description="Update currency of the ticket.", examples=["EUR"]
    )
    description: str | None = Field(None, max_length=500)


class TicketResponse(BaseModel):
    """Schema for returning ticket data."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    cost: float
    currency: Currency
    event_id: str
    description: str | None
    creation_date: CustomDateTime
    update_date: CustomDateTime | None
