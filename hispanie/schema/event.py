from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..model import EventCategory
from ..typing import CustomDateTime
from .file import FileBasicResponse, FileCreateRequest
from .tag import TagBasicResponse


class EventCreateRequest(BaseModel):
    """
    Schema for creating a new Event.
    """

    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr | None = Field(None, description="Valid email address")
    phone: str | None = Field(None, pattern=r"^\+?[0-9\s-]+$", description="Valid phone number")
    city: str = Field(..., min_length=2, max_length=50)
    address: str = Field(..., min_length=5, max_length=200)
    country: str = Field(..., min_length=2, max_length=50)
    municipality: str = Field(..., min_length=2, max_length=50)
    postcode: str = Field(..., min_length=2, max_length=20)
    region: str = Field(..., min_length=2, max_length=50)
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees")
    category: EventCategory
    is_public: bool = Field(default=False, description="Whether the event is public or not")
    description: str | None = Field(None, max_length=500)
    price: float = Field(..., ge=0.0, description="Price of the event")
    start_date: datetime = Field(..., description="Start date of the event")
    end_date: datetime = Field(..., description="End date of the event")
    files: list[FileCreateRequest] = Field(
        default_factory=list[FileCreateRequest],
        description="List of files associated with the event",
    )
    tags: list[TagBasicResponse] = Field(
        default_factory=list[TagBasicResponse], description="List of tags associated with the event"
    )
    urls: list[str] = Field(
        default_factory=list[str], description="List of URLs associated with the event"
    )


class EventUpdateRequest(BaseModel):
    """
    Schema for updating an existing Event.
    """

    name: str | None = Field(None, min_length=3, max_length=100)
    email: EmailStr | None = Field(None, description="Valid email address")
    phone: str | None = Field(None, pattern=r"^\+?[0-9\s-]+$", description="Valid phone number")
    address: str | None = Field(None, min_length=5, max_length=200)
    country: str | None = Field(None, min_length=2, max_length=50)
    municipality: str | None = Field(None, min_length=2, max_length=50)
    city: str | None = Field(None, min_length=2, max_length=50)
    postcode: str | None = Field(None, min_length=2, max_length=20)
    region: str | None = Field(None, min_length=2, max_length=50)
    latitude: float | None = Field(
        None, ge=-90.0, le=90.0, description="Latitude in decimal degrees"
    )
    longitude: float | None = Field(
        None, ge=-180.0, le=180.0, description="Longitude in decimal degrees"
    )
    category: EventCategory | None = None
    is_public: bool | None = Field(None, description="Whether the event is public or not")
    description: str | None = Field(None, max_length=500)
    price: float | None = Field(None, ge=0.0, description="Price of the event")
    start_date: datetime | None = Field(None, description="Start date of the event")
    end_date: datetime | None = Field(None, description="End date of the event")
    files: list[FileCreateRequest] | None = Field(
        default_factory=None, description="List of files associated with the event"
    )
    tags: list[TagBasicResponse] | None = Field(
        default=None, description="List of tags associated with the event"
    )
    urls: list[str] | None = Field(
        default=None, description="List of URLs associated with the event"
    )


class EventResponse(BaseModel):
    """
    Schema for returning Event data.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str | None
    phone: str | None
    address: str
    city: str
    latitude: float
    longitude: float
    category: EventCategory
    is_public: bool
    description: str | None
    price: float
    start_date: CustomDateTime
    end_date: CustomDateTime
    files: list[FileBasicResponse]
    tags: list[TagBasicResponse]
    urls: list[str]
    creation_date: CustomDateTime
    update_date: CustomDateTime | None
