from fastapi import APIRouter, HTTPException

from ...action.event import create as create_event
from ...schema import EventCreateRequest

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Not found"}},
)


# TODO add authentification + retrive account + add account to create event
@router.post("/", response_model=EventCreateRequest)
async def create(event_data: EventCreateRequest):
    try:
        return create_event(event_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating event: {str(e)}")
