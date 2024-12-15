from typing import List

from pydantic import BaseModel, Field

from ..typing import CustomDateTime


class TagCreateRequest(BaseModel):
    """
    Schema for creating a new Tag.
    """

    name: str = Field(..., min_length=1, max_length=100, description="Unique name of the tag.")
    description: str | None = Field(None, min_length=5, max_length=1000)


class TagUpdateRequest(BaseModel):
    """
    Schema for updating an existing Tag.
    """

    name: str | None = Field(
        None, min_length=1, max_length=100, description="Updated name of the tag."
    )
    description: str | None = Field(None, min_length=5, max_length=1000)


class TagResponse(BaseModel):
    """
    Schema for returning Tag data.
    """

    id: str
    name: str
    description: str | None
    creation_date: CustomDateTime
    update_date: CustomDateTime | None
    events: List[str] = Field(
        default_factory=list, description="List of event IDs associated with this tag."
    )
    businesses: List[str] = Field(
        default_factory=list, description="List of business IDs associated with this tag."
    )

    class Config:
        from_attributes = True
