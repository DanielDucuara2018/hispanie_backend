import logging

from ..model import Event, File, Tag
from ..schema import EventCreateRequest, EventUpdateRequest
from ..utils import ensure_user_owns_resource
from .account import read as read_accounts
from .tag import read as read_tags

logger = logging.getLogger(__name__)


def create(event_data: EventCreateRequest, account_id: str) -> Event:
    account = read_accounts(account_id)
    data = event_data.model_dump()
    logger.info("Adding new event: %s", data)
    # Format and check tags
    files = [File(account=account, **file).create() for file in data.pop("files")]
    tags = read_tags(id=[tag["id"] for tag in data.pop("tags")])
    event = Event(account=account, tags=tags, files=files, **data).create()
    logger.info("Added new event: %s", event.id)
    return event


def read(event_id: str | None = None, **kwargs) -> Event | list[Event]:
    if event_id:
        logger.info("Reading event: %s", event_id)
        return Event.get(id=event_id)
    else:
        logger.info("Reading all events")
        return Event.find(**kwargs)


def update(event_id: str, account_id: str, event_data: EventUpdateRequest) -> Event:
    event = Event.get(id=event_id)
    ensure_user_owns_resource(account_id, event.account_id)
    data = event_data.model_dump(exclude_none=True)
    logger.info("Updating event: %s with %s", event_id, data)
    # Format and check tags
    if tags := data.pop("tags", []):
        data["tags"] = [Tag.get(id=t) for t in tags]
    result = event.update(**data)
    logger.info("Updated event: %s", event_id)
    return result


def delete(event_id: str, account_id: str) -> Event:
    logger.info("Deleting event: %s", event_id)
    event = Event.get(id=event_id)
    ensure_user_owns_resource(account_id, event.account_id)
    result = event.delete()
    logger.info("Deleted event: %s", event_id)
    return result
