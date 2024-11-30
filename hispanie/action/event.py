import logging

from ..model import Event, EventCategory
from ..schema import EventCreateRequest

logger = logging.getLogger(__name__)


def create(event_data: EventCreateRequest) -> Event:
    logger.info("Adding new account")
    event = Event(
        name=event_data.name,
        description=event_data.description,
        city=event_data.city,
        latitude=event_data.latitude,
        longitude=event_data.longitude,
        type=EventCategory(event_data.type),
        is_public=event_data.is_public,
    ).create()
    logger.info("Added new user %s", event.id)
    return event
