from pydantic import BaseModel, ConfigDict, Field

from ..model.file import FileCategory
from ..typing import CustomDateTime


class FileGeneratePresignedUrlResponse(BaseModel):
    """
    Schema for creating a presigned url to upload on AWS.
    """

    url: str


class FileCreateRequest(BaseModel):
    """
    Schema for creating a new File.
    """

    filename: str = Field(..., min_length=3, max_length=100)
    content_type: str = Field(..., min_length=3, max_length=100)
    category: FileCategory
    path: str = Field(..., min_length=3, max_length=1000)
    description: str | None = Field(None, min_length=5, max_length=1000)


class FileUpdateRequest(BaseModel):
    """
    Schema for updating an existing File.
    """

    filename: str | None = Field(None, min_length=3, max_length=100)
    content_type: str | None = Field(None, min_length=3, max_length=100)
    category: FileCategory | None
    path: str = Field(None, min_length=3, max_length=1000)
    description: str | None = Field(None, min_length=5, max_length=1000)


# Schema for Account Response
class FileResponse(BaseModel):
    """
    Schema for returning File data.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    path: str
    content_type: str
    category: FileCategory
    path: str
    description: str | None
    creation_date: CustomDateTime
    update_date: CustomDateTime | None
