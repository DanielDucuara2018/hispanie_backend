from fastapi import APIRouter, Depends, HTTPException

from ...action import (
    create_ticket,
    delete_ticket,
    get_current_account,
    read_tickets,
    update_ticket,
)
from ...schema import TicketCreateRequest, TicketResponse, TicketUpdateRequest

router = APIRouter(
    prefix="/ticket",
    tags=["ticket"],
    responses={400: {"description": "Not found"}},
)


@router.post("/private/create", response_model=TicketResponse)
async def create(
    ticket_data: TicketCreateRequest,
    _: None = Depends(get_current_account),
):
    """Create a new ticket for the authenticated account."""
    try:
        return create_ticket(ticket_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating ticket: {str(e)}")


@router.get("/private/read", response_model=list[TicketResponse])
async def read(
    event_id: str | None = None,
    _: None = Depends(get_current_account),
):
    """Retrieve all tickets for the authenticated account."""
    try:
        return read_tickets(**({"event_id": event_id} if event_id else {}))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving tickets: {str(e)}")


@router.put("/private/update/{ticket_id}", response_model=TicketResponse)
async def update(
    ticket_id: str,
    ticket_update: TicketUpdateRequest,
    _: None = Depends(get_current_account),
):
    """Update a ticket by its id."""
    try:
        return update_ticket(ticket_id=ticket_id, ticket_data=ticket_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating ticket: {str(e)}")


@router.delete("/private/delete/{ticket_id}", response_model=TicketResponse)
async def delete(
    ticket_id: str,
    _: None = Depends(get_current_account),
):
    """Delete a ticket by its id."""
    try:
        return delete_ticket(ticket_id=ticket_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting ticket: {str(e)}")
