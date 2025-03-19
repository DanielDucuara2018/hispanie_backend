from typing import overload

from ..config import logging
from ..model import Event, Ticket
from ..schema import TicketCreateRequest, TicketUpdateRequest

logger = logging.getLogger(__name__)


def create(ticket_data: TicketCreateRequest) -> Ticket:
    # Check event
    Event.get(id=ticket_data.event_id)

    if activities := read(event_id=ticket_data.event_id, name=ticket_data.name):
        logger.info("Ticket already exists: %s", activities[0].id)
        return activities[0]

    logger.info("Adding new ticket: %s", ticket_data)
    ticket = Ticket(**ticket_data.model_dump()).create()
    logger.info("Added new ticket: %s", ticket.id)
    return ticket


@overload
def read(ticket_id: str) -> Ticket: ...
@overload
def read(**kwargs) -> list[Ticket]: ...
def read(ticket_id: str | None = None, **kwargs) -> Ticket | list[Ticket]:
    if ticket_id:
        logger.info("Reading ticket: %s", ticket_id)
        return Ticket.get(id=ticket_id)
    else:
        logger.info("Reading all tickets with filters %s", kwargs)
        return Ticket.find(**kwargs)


def update(ticket_id: str, ticket_data: TicketUpdateRequest) -> Ticket:
    logger.info("Updating ticket: %s with %s", ticket_id, ticket_data)
    tag = Ticket.get(id=ticket_id)
    result = tag.update(**ticket_data.model_dump(exclude_none=True))
    logger.info("Updated ticket: %s", ticket_id)
    return result


def delete(ticket_id: str) -> Ticket:
    logger.info("Deleting ticket: %s", ticket_id)
    activity = Ticket.get(id=ticket_id)
    result = activity.delete()
    logger.info("Deleted ticket: %s", ticket_id)
    return result
