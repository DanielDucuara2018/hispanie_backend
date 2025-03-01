from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..model import BusinessCategory
from ..typing import CustomDateTime


class BusinessCreateRequest(BaseModel):
    """
    Schema for creating a new Business.
    """

    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr = Field(..., description="Valid email address")
    phone: str = Field(..., pattern=r"^\+?[0-9\s-]+$", description="Valid phone number")
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
    is_public: bool = Field(default=False, description="Whether the business is public or not")
    category: BusinessCategory
    description: str | None = Field(None, min_length=5, max_length=1000)
    files: list["FileCreateRequest"] = Field(
        default_factory=list["FileCreateRequest"],
        description="List of files associated with the event",
    )
    tags: list["TagBasicResponse"] = Field(
        default_factory=list["TagBasicResponse"],
        description="List of tags associated with the event",
    )
    social_networks: list["SocialNetworkCreateRequest"] = Field(
        default_factory=list["SocialNetworkCreateRequest"],
        description="List of URLs associated with the event",
    )


class BusinessUpdateRequest(BaseModel):
    """
    Schema for updating an existing Business.
    """

    name: str | None = Field(None, min_length=3, max_length=100)
    email: EmailStr | None = Field(None, description="Valid email address")
    phone: str | None = Field(None, pattern=r"^\+?[0-9\s-]+$", description="Valid phone number")
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
    category: BusinessCategory | None = None
    description: str | None = Field(None, min_length=5, max_length=1000)
    files: list["FileCreateRequest"] | None = Field(
        default=None, description="List of files associated with the event"
    )
    tags: list["TagBasicResponse"] | None = Field(
        default=None, description="List of tags associated with the event"
    )
    social_networks: list["SocialNetworkCreateRequest"] | None = Field(
        default=None, description="List of URLs associated with the event"
    )


class BusinessResponse(BaseModel):
    """
    Schema for returning Business data.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    email: str
    phone: str
    address: str | None
    country: str | None
    municipality: str | None
    city: str | None
    postcode: str | None
    region: str | None
    latitude: float | None
    longitude: float | None
    is_public: bool
    category: BusinessCategory
    description: str | None
    files: list["FileBasicResponse"]
    tags: list["TagBasicResponse"]
    social_networks: list["SocialNetworkBasicResponse"]
    creation_date: CustomDateTime
    update_date: CustomDateTime | None


from .file import FileBasicResponse, FileCreateRequest  # noqa: E402
from .social_network import SocialNetworkBasicResponse, SocialNetworkCreateRequest  # noqa: E402
from .tag import TagBasicResponse  # noqa: E402
