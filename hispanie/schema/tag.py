from pydantic import BaseModel, ConfigDict, Field

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

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None
    creation_date: CustomDateTime
    update_date: CustomDateTime | None
    events_ids: list[str] = Field(
        default_factory=list, description="List of event IDs associated with this tag."
    )
    businesses_ids: list[str] = Field(
        default_factory=list, description="List of business IDs associated with this tag."
    )


class TagBasicResponse(BaseModel):
    """
    Schema for returning Tag basic data.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
