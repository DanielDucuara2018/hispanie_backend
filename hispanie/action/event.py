import logging

from ..model import Event
from ..schema import EventCreateRequest, EventUpdateRequest
from .account import read as read_account

logger = logging.getLogger(__name__)


# Helper function for error handling
def ensure_user_owns_event(current_account_id: int, event_owner_id: int) -> None:
    """
    Raise an exception if the current account does not own the event.
    """
    if current_account_id != event_owner_id:
        raise Exception("You do not have permission to access this event.")


def create(event_data: EventCreateRequest, account_id: str) -> Event:
    logger.info("Adding new event %s", event_data)
    account = read_account(account_id)
    event = Event(account=account, **event_data.model_dump()).create()
    logger.info("Added new event %s", event.id)
    return event


def read(event_id: str | None = None, **kwargs) -> Event | list[Event]:
    if event_id:
        logger.info("Reading %s data", event_id)
        result = Event.get(id=event_id)
    else:
        logger.info("Reading all data")
        result = Event.find(**kwargs)
    return result


def update(event_id: str, account_id: str, event_data: EventUpdateRequest) -> Event:
    logger.info("Updating %s event", event_id)
    event = Event.get(id=event_id)
    ensure_user_owns_event(account_id, event.account_id)
    result = event.update(**event_data.model_dump(exclude_none=True))
    logger.info("Updated event %s", event_id)
    return result


def delete(event_id: str, account_id: str) -> Event:
    logger.info("Deleting %s event", event_id)
    event = Event.get(id=event_id)
    ensure_user_owns_event(account_id, event.account_id)
    result = event.delete()
    logger.info("Deleted event %s", event_id)
    return result
