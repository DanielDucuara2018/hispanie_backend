from pydantic import BaseModel, Field

from ..model import EventCategory


class EventCreateUpdateRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    city: str = Field(..., min_length=2, max_length=50)
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees")
    type: EventCategory
    is_public: bool = Field(default=False, description="Whether the event is public or not")
    description: str | None = Field(None, max_length=500)


class EventResponse(BaseModel):
    id: str
    name: str
    city: str
    latitude: float
    longitude: float
    type: EventCategory
    is_public: bool
    description: str | None

    class Config:
        orm_mode = True
