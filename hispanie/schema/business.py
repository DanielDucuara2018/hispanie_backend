from pydantic import BaseModel, EmailStr, Field

from ..model import BusinessCategory
from ..typing import CustomDateTime


class BusinessCreateRequest(BaseModel):
    """
    Schema for creating a new Business.
    """

    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr | None = Field(None, description="Valid email address")
    phone: str | None = Field(None, pattern="^\+?[0-9\s-]+$", description="Valid phone number")
    address: str = Field(..., min_length=5, max_length=200)
    country: str = Field(..., min_length=2, max_length=50)
    municipality: str = Field(..., min_length=2, max_length=50)
    city: str = Field(..., min_length=2, max_length=50)
    postcode: str = Field(..., min_length=2, max_length=20)
    region: str = Field(..., min_length=2, max_length=50)
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees")
    is_public: bool = Field(default=False, description="Whether the business is public or not")
    category: BusinessCategory
    description: str | None = Field(None, min_length=5, max_length=1000)
    tags: list[str] | None = Field(
        default_factory=list, description="List of tags associated with the event"
    )
    urls: list[str] | None = Field(
        default_factory=list, description="List of URLs associated with the event"
    )


class BusinessUpdateRequest(BaseModel):
    """
    Schema for updating an existing Business.
    """

    name: str | None = Field(None, min_length=3, max_length=100)
    email: EmailStr | None = Field(None, description="Valid email address")
    phone: str | None = Field(None, pattern="^\+?[0-9\s-]+$", description="Valid phone number")
    address: str | None = Field(None, min_length=5, max_length=200)
    country: str | None = Field(None, min_length=2, max_length=50)
    municipality: str | None = Field(None, min_length=2, max_length=50)
    city: str | None = Field(None, min_length=2, max_length=50)
    postcode: str | None = Field(None, min_length=2, max_length=20)
    region: str | None = Field(None, min_length=2, max_length=50)
    latitude: float | None = Field(
        None, ge=-90.0, le=90.0, description="Latitude in decimal degrees"
    )
    longitude: float | None = Field(
        None, ge=-180.0, le=180.0, description="Longitude in decimal degrees"
    )
    is_public: bool | None = Field(None, description="Whether the business is public or not")
    category: BusinessCategory | None
    description: str | None = Field(None, min_length=5, max_length=1000)
    tags: list[str] | None = Field(
        default_factory=list, description="List of tags associated with the event"
    )
    urls: list[str] | None = Field(
        default_factory=list, description="List of URLs associated with the event"
    )


class BusinessResponse(BaseModel):
    """
    Schema for returning Business data.
    """

    id: str
    name: str
    email: str | None
    phone: str | None
    address: str
    country: str
    municipality: str
    city: str
    postcode: str
    region: str
    latitude: float
    longitude: float
    is_public: bool
    category: BusinessCategory
    description: str | None
    # tags: list[str] #TODO fix {'type': 'list_type', 'loc': ('response', 'urls'), 'msg': 'Input should be a valid list', 'input': '{}'}
    # urls: list[str]
    creation_date: CustomDateTime
    update_date: CustomDateTime | None

    class Config:
        from_attributes = True