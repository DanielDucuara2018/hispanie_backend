from pydantic import BaseModel, ConfigDict, Field

from ..model.file import FileCategory
from ..typing import CustomDateTime


class FileGeneratePresignedUrlResponse(BaseModel):
    """Schema for creating a presigned url to upload on AWS."""

    url: str


class FileCreateRequest(BaseModel):
    """Schema for creating a new File."""

    filename: str = Field(..., min_length=3, max_length=100)
    content_type: str = Field(..., min_length=3, max_length=100)
    category: FileCategory
    path: str = Field(..., min_length=3, max_length=1000)
    hash: str = Field(..., min_length=3, max_length=1000)
    description: str | None = Field(None, min_length=5, max_length=1000)


class FileUpdateRequest(BaseModel):
    """Schema for updating an existing File."""

    id: str | None = Field(None, min_length=3, max_length=100)
    filename: str | None = Field(None, min_length=3, max_length=100)
    content_type: str | None = Field(None, min_length=3, max_length=100)
    category: FileCategory | None
    path: str | None = Field(None, min_length=3, max_length=1000)
    hash: str | None = Field(..., min_length=3, max_length=1000)
    description: str | None = Field(None, min_length=5, max_length=1000)


# Schema for Account Response
class FileResponse(BaseModel):
    """Schema for returning File data."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    path: str
    hash: str
    content_type: str
    category: FileCategory
    description: str | None
    creation_date: CustomDateTime
    update_date: CustomDateTime | None
    events: list["EventResponse"] = Field(
        default_factory=list["EventResponse"],
        description="List of events associated with this tag.",
    )
    businesses: list["BusinessResponse"] = Field(
        default_factory=list["BusinessResponse"],
        description="List of business associated with this tag.",
    )


class FileBasicResponse(BaseModel):
    """Schema for returning File data."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    path: str
    hash: str
    category: FileCategory
    creation_date: CustomDateTime
    update_date: CustomDateTime | None


from .business import BusinessResponse  # noqa: E402
from .event import EventResponse  # noqa: E402
