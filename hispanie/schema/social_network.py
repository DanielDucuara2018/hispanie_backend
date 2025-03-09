from pydantic import BaseModel, ConfigDict, Field

from ..model.social_network import SocialNetworkCategory
from ..typing import CustomDateTime


class SocialNetworkCreateRequest(BaseModel):
    """Schema for adding a new Social Network ulr."""

    url: str = Field(..., min_length=3, max_length=1000)
    category: SocialNetworkCategory


class SocialNetworkBasicResponse(BaseModel):
    """Schema for returning File data."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    url: str
    category: SocialNetworkCategory
    creation_date: CustomDateTime
    update_date: CustomDateTime | None
