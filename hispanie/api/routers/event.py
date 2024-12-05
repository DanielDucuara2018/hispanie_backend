from typing import List

from fastapi import APIRouter, Depends, HTTPException

from hispanie.schema import AccountResponse

from ...action import create_event, delete_event, get_current_account, read_events, update_event
from ...schema import EventCreateUpdateRequest, EventResponse

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


# Create Event
@router.post("/", response_model=EventResponse)
async def create(
    event_data: EventCreateUpdateRequest,
    current_account: AccountResponse = Depends(get_current_account),
):
    """
    Create a new event for the authenticated user.
    """
    try:
        return create_event(event_data, current_account.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating event: {str(e)}")


# Read Events
@router.get("/", response_model=List[EventResponse])
async def read(
    current_account: AccountResponse = Depends(get_current_account),
):
    """
    Retrieve all events for the authenticated user.
    """
    try:
        return read_events(account_id=current_account.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving events: {str(e)}")


# Update Event
@router.put("/{event_id}", response_model=EventResponse)
async def update(
    event_id: int,
    event_update: EventCreateUpdateRequest,
    current_account: AccountResponse = Depends(get_current_account),
):
    """
    Update an event by its ID. The event must belong to the current user.
    """
    try:
        return update_event(event_id, current_account.id, event_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating event: {str(e)}")


# Delete Event
@router.delete("/{event_id}", response_model=EventResponse)
async def delete(
    event_id: int,
    current_account: AccountResponse = Depends(get_current_account),
):
    """
    Delete an event by its ID. The event must belong to the current user.
    """
    try:
        return delete_event(event_id, current_account.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting event: {str(e)}")
