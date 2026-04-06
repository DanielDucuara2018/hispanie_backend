from typing import overload

from hispanie.action.account import read as read_accounts
from hispanie.action.tag import read as read_tags
from hispanie.config import logging
from hispanie.model import Activity, Event, File, Tag, Ticket
from hispanie.schema import EventCreateRequest, EventUpdateRequest
from hispanie.utils import (
    delete_duplicates,
    ensure_user_owns_resource,
    handle_update_files,
    handle_update_resources,
)

logger = logging.getLogger(__name__)


async def create(event_data: EventCreateRequest, account_id: str) -> Event:
    account = await read_accounts(account_id)
    data = event_data.model_dump()
    logger.info("Adding new event: %s", data)
    activities = [Activity(**act) for act in delete_duplicates(data.pop("activities"), "name")]
    files = [await File(**file).create() for file in data.pop("files")]
    tags = await read_tags(id=[tag["id"] for tag in data.pop("tags")])
    tickets = [Ticket(**tic) for tic in delete_duplicates(data.pop("tickets"), "name")]
    event = await Event(
        account=account,
        activities=activities,
        files=files,
        tags=tags,
        tickets=tickets,
        **data,
    ).create()
    logger.info("Added new event: %s", event.id)
    return event


@overload
async def read(event_id: str) -> Event: ...
@overload
async def read(**kwargs) -> list[Event]: ...
async def read(event_id: str | None = None, **kwargs) -> Event | list[Event]:
    if event_id:
        logger.info("Reading event: %s", event_id)
        return await Event.get(id=event_id)
    else:
        logger.info("Reading all events")
        return await Event.find(**kwargs)


async def update(event_id: str, account_id: str, event_data: EventUpdateRequest) -> Event:
    event = await Event.get(id=event_id)
    ensure_user_owns_resource(account_id, event.account_id)
    data = event_data.model_dump(exclude_none=True)
    logger.info("Updating event: %s with %s", event_id, data)
    if activities := data.pop("activities", []):
        data["activities"] = await handle_update_resources(
            activities,
            event.activities,
            Activity,
            remove_duplicates=True,
        )
    if files := data.pop("files", []):
        data["files"] = await handle_update_files(files, File)
    if tags := data.pop("tags", []):
        data["tags"] = [await Tag.get(id=t["id"]) for t in tags]
    if tickets := data.pop("tickets", []):
        data["tickets"] = await handle_update_resources(
            tickets,
            event.tickets,
            Ticket,
            remove_duplicates=True,
        )
    result = await event.update(**data)
    logger.info("Updated event: %s", event_id)
    return result


async def delete(event_id: str, account_id: str) -> Event:
    logger.info("Deleting event: %s", event_id)
    event = await Event.get(id=event_id)
    ensure_user_owns_resource(account_id, event.account_id)
    result = await event.delete()
    logger.info("Deleted event: %s", event_id)
    return result
