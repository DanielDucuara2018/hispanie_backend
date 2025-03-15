from fastapi import APIRouter, Depends, HTTPException

from ...action import (
    create_activity,
    delete_activity,
    get_current_account,
    read_activities,
    update_activity,
)
from ...schema import ActivityCreateRequest, ActivityResponse, ActivityUpdateRequest

router = APIRouter(
    prefix="/activity",
    tags=["activity"],
    responses={400: {"description": "Not found"}},
)


@router.post("/private/create", response_model=ActivityResponse)
async def create(
    activity_data: ActivityCreateRequest,
    _: None = Depends(get_current_account),
):
    """Create a new activity for the authenticated account."""
    try:
        return create_activity(activity_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating activity: {str(e)}")


@router.get("/private/read", response_model=list[ActivityResponse])
async def read(
    event_id: str | None = None,
    _: None = Depends(get_current_account),
):
    """Retrieve all activities for the authenticated account."""
    try:
        return read_activities(**({"event_id": event_id} if event_id else {}))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving activities: {str(e)}")


@router.put("/private/update/{activity_id}", response_model=ActivityResponse)
async def update(
    activity_id: str,
    activity_update: ActivityUpdateRequest,
    _: None = Depends(get_current_account),
):
    """Update an activity by its id."""
    try:
        return update_activity(activity_id=activity_id, activity_data=activity_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating activity: {str(e)}")


@router.delete("/private/delete/{activity_id}", response_model=ActivityResponse)
async def delete(
    activity_id: str,
    _: None = Depends(get_current_account),
):
    """Delete an activity by its id."""
    try:
        return delete_activity(activity_id=activity_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting activity: {str(e)}")
