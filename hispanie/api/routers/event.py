from fastapi import APIRouter, Depends, HTTPException

from hispanie.schema import AccountResponse

from ...action import create_event, delete_event, get_current_account, read_events, update_event
from ...schema import EventCreateRequest, EventResponse, EventUpdateRequest

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


# Create Event using token
@router.post("/private/create", response_model=EventResponse)
async def create(
    event_data: EventCreateRequest,
    current_account: AccountResponse = Depends(get_current_account),
):
    """
    Create a new event for the authenticated account.
    """
    try:
        return create_event(event_data, current_account.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating event: {str(e)}")


# Read Events using token
@router.get("/private/read", response_model=list[EventResponse])
async def read_private(
    current_account: AccountResponse = Depends(get_current_account),
):
    """
    Retrieve all events for the authenticated account.
    """
    try:
        return read_events(account_id=current_account.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving events: {str(e)}")


# Read Events using token
@router.get("/public/read", response_model=list[EventResponse])
async def read_public():
    """
    Retrieve all events for the authenticated account.
    """
    try:
        return read_events(is_public=True)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving events: {str(e)}")


# Update Event
@router.put("/private/update/{event_id}", response_model=EventResponse)
async def update(
    event_id: str,
    event_update: EventUpdateRequest,
    current_account: AccountResponse = Depends(get_current_account),
):
    """
    Update an event by its ID. The event must belong to the current account.
    """
    try:
        return update_event(event_id, current_account.id, event_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating event: {str(e)}")


# Delete Event
@router.delete("/private/delete/{event_id}", response_model=EventResponse)
async def delete(
    event_id: str,
    current_account: AccountResponse = Depends(get_current_account),
):
    """
    Delete an event by its ID. The event must belong to the current account.
    """
    try:
        return delete_event(event_id, current_account.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting event: {str(e)}")
