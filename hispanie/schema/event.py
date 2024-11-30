from pydantic import BaseModel

from ..model import EventCategory


class EventCreateRequest(BaseModel):
    name: str
    city: str
    latitude: float
    longitude: float
    type: EventCategory
    is_public: bool = False
    description: str | None = None
