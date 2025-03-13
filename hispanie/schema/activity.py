from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from ..typing import CustomDateTime


class ActivityBasicCreateRequest(BaseModel):
    """Schema for creating a new activity without event_id."""

    name: str = Field(..., min_length=1, max_length=500, description="Unique name of the activity.")
    description: str | None = Field(None, max_length=500)
    start_date: datetime = Field(
        ..., description="Start date of the activity", examples=["2025-03-09T11:40:22.503Z"]
    )
    end_date: datetime = Field(
        ..., description="End date of the activity", examples=["2025-03-15T11:40:22.503Z"]
    )


class ActivityCreateRequest(BaseModel):
    """Schema for creating a new activity."""

    name: str = Field(..., min_length=1, max_length=500, description="Unique name of the activity.")
    event_id: str = Field(..., pattern=r"^event-[0-9a-f]{32}$")
    description: str | None = Field(None, max_length=500)
    start_date: datetime = Field(..., description="Start date of the activity")
    end_date: datetime = Field(..., description="End date of the activity")


class ActivityUpdateRequest(BaseModel):
    """Schema for updating an activity."""

    id: str | None = Field(None, pattern=r"^activity-[0-9a-f]{32}$")
    name: str | None = Field(
        None, min_length=1, max_length=500, description="Update name of the activity."
    )
    description: str | None = Field(None, max_length=500)
    start_date: datetime | None = Field(None, description="Start date of the activity")
    end_date: datetime | None = Field(None, description="End date of the activity")


class ActivityResponse(BaseModel):
    """Schema for returning activity data."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str | None
    event_id: str
    creation_date: CustomDateTime
    start_date: CustomDateTime
    end_date: CustomDateTime
    update_date: CustomDateTime | None
