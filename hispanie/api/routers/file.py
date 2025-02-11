from fastapi import APIRouter, Depends, HTTPException

from hispanie.schema import AccountResponse

from ...action import (
    create_file,
    delete_file,
    generate_download_presigned_url,
    generate_upload_presigned_url,
    get_current_account,
    read_files,
    update_file,
)
from ...schema import (
    FileCreateRequest,
    FileGeneratePresignedUrlResponse,
    FileResponse,
    FileUpdateRequest,
)

router = APIRouter(
    prefix="/files",
    tags=["files"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/private/generate-upload-presigned-url", response_model=FileGeneratePresignedUrlResponse
)
async def upload_presigned_url(
    filename: str,
    content_type: str,
    _: None = Depends(get_current_account),
):
    """
    Create a new event for the authenticated account.
    """
    try:
        return {"url": generate_upload_presigned_url(filename, content_type)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating event: {str(e)}")


@router.get(
    "/private/generate-download-presigned-url", response_model=FileGeneratePresignedUrlResponse
)
async def download_presigned_url(
    filename: str,
    _: None = Depends(get_current_account),
):
    """
    Create a new event for the authenticated account.
    """
    try:
        return {"url": generate_download_presigned_url(filename)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating event: {str(e)}")


# Create Event using token
@router.post("/private/create", response_model=FileResponse)
async def create(
    file_data: FileCreateRequest,
    current_account: AccountResponse = Depends(get_current_account),
):
    """
    Create a new event for the authenticated account.
    """
    try:
        return create_file(file_data, current_account.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating event: {str(e)}")


# TODO confirm if it's usefull
# Read Events using token
@router.get("/private/read", response_model=list[FileResponse])
async def read_private(
    current_account: AccountResponse = Depends(get_current_account),
):
    """
    Retrieve all events for the authenticated account.
    """
    try:
        return read_files(account_id=current_account.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving events: {str(e)}")


# TODO confirm if it's usefull
# Read Events using token
@router.get("/public/read", response_model=list[FileResponse])
async def read_public():
    """
    Retrieve all events for the authenticated account.
    """
    try:
        return read_files(is_public=True)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving events: {str(e)}")


# Update Event
@router.put("/private/update/{file_id}", response_model=FileResponse)
async def update(
    file_id: str,
    event_update: FileUpdateRequest,
    current_account: AccountResponse = Depends(get_current_account),
):
    """
    Update an event by its ID. The event must belong to the current account.
    """
    try:
        return update_file(file_id, current_account.id, event_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating event: {str(e)}")


# Delete Event
@router.delete("/private/delete/{file_id}", response_model=FileResponse)
async def delete(
    file_id: str,
    current_account: AccountResponse = Depends(get_current_account),
):
    """
    Delete an event by its ID. The event must belong to the current account.
    """
    try:
        return delete_file(file_id, current_account.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting event: {str(e)}")
