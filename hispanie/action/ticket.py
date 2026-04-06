from typing import overload

from hispanie.config import logging
from hispanie.model import Event, Ticket
from hispanie.schema import TicketCreateRequest, TicketUpdateRequest

logger = logging.getLogger(__name__)


async def create(ticket_data: TicketCreateRequest) -> Ticket:
    await Event.get(id=ticket_data.event_id)

    if activities := await read(event_id=ticket_data.event_id, name=ticket_data.name):
        logger.info("Ticket already exists: %s", activities[0].id)
        return activities[0]

    logger.info("Adding new ticket: %s", ticket_data)
    ticket = await Ticket(**ticket_data.model_dump()).create()
    logger.info("Added new ticket: %s", ticket.id)
    return ticket


@overload
async def read(ticket_id: str) -> Ticket: ...
@overload
async def read(**kwargs) -> list[Ticket]: ...
async def read(ticket_id: str | None = None, **kwargs) -> Ticket | list[Ticket]:
    if ticket_id:
        logger.info("Reading ticket: %s", ticket_id)
        return await Ticket.get(id=ticket_id)
    else:
        logger.info("Reading all tickets with filters %s", kwargs)
        return await Ticket.find(**kwargs)


async def update(ticket_id: str, ticket_data: TicketUpdateRequest) -> Ticket:
    logger.info("Updating ticket: %s with %s", ticket_id, ticket_data)
    tag = await Ticket.get(id=ticket_id)
    result = await tag.update(**ticket_data.model_dump(exclude_none=True))
    logger.info("Updated ticket: %s", ticket_id)
    return result


async def delete(ticket_id: str) -> Ticket:
    logger.info("Deleting ticket: %s", ticket_id)
    activity = await Ticket.get(id=ticket_id)
    result = await activity.delete()
    logger.info("Deleted ticket: %s", ticket_id)
    return result
