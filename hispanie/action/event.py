import logging

from ..model import Activity, Event, File, Tag
from ..schema import EventCreateRequest, EventUpdateRequest
from ..utils import (
    delete_duplicates,
    ensure_user_owns_resource,
    handle_update_files,
    handle_update_resources,
)
from .account import read as read_accounts
from .tag import read as read_tags

logger = logging.getLogger(__name__)


def create(event_data: EventCreateRequest, account_id: str) -> Event:
    account = read_accounts(account_id)
    data = event_data.model_dump()
    logger.info("Adding new event: %s", data)
    # Format and check extra models
    activities = [Activity(**act) for act in delete_duplicates(data.pop("activities"), "name")]
    files = [File(**file).create() for file in data.pop("files")]
    tags = read_tags(id=[tag["id"] for tag in data.pop("tags")])
    event = Event(
        account=account,
        activities=activities,
        files=files,
        tags=tags,
        **data,
    ).create()
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
    if activities := data.pop("activities", []):
        data["activities"] = handle_update_resources(
            activities,
            event.activities,
            Activity,
            remove_duplicates=True,
        )
    if files := data.pop("files", []):
        data["files"] = handle_update_files(files, File)
    if tags := data.pop("tags", []):
        data["tags"] = [Tag.get(id=t["id"]) for t in tags]
    result = event.update(**data)
    logger.info("Updated event: %s", event_id)
    return result


def delete(event_id: str, account_id: str) -> Event:
    logger.info("Deleting event: %s", event_id)
    event = Event.get(id=event_id)
    # TODO add adming account can delete whateve it wants
    ensure_user_owns_resource(account_id, event.account_id)
    result = event.delete()
    logger.info("Deleted event: %s", event_id)
    return result
