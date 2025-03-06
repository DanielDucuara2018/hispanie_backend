from fastapi import APIRouter, Depends, HTTPException

from ...action import create_tag, delete_tag, get_current_account, read_tags, update_tag
from ...schema import TagCreateRequest, TagResponse, TagUpdateRequest

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    responses={400: {"description": "Not found"}},
)


# Create Tag using token
@router.post("/private/create", response_model=TagResponse)
async def create(
    tag_data: TagCreateRequest,
    _: None = Depends(get_current_account),
):
    """Create a new tag for the authenticated account."""
    try:
        return create_tag(tag_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating tag: {str(e)}")


# Read Tags using token
@router.get("/private/read", response_model=list[TagResponse])
async def read(
    _: None = Depends(get_current_account),
):
    """Retrieve all tag for the authenticated account."""
    try:
        return read_tags()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving tags: {str(e)}")


# Update Tag
@router.put("/private/update/{tag_id}", response_model=TagResponse)
async def update(
    tag_id: str,
    tag_update: TagUpdateRequest,
    _: None = Depends(get_current_account),
):
    """Update a tag by its ID."""
    try:
        return update_tag(tag_id, tag_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating tag: {str(e)}")


# Delete Tag
@router.delete("/private/delete/{tag_id}", response_model=TagResponse)
async def delete(
    tag_id: str,
    _: None = Depends(get_current_account),
):
    """Delete a tag by its ID."""
    try:
        return delete_tag(tag_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting tag: {str(e)}")
