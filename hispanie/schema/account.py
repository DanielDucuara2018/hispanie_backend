from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..model import AccountType
from ..typing import CustomDateTime


class Token(BaseModel):
    """Schema for returning Token data."""

    access_token: str
    token_type: str
    token_expiration_date: CustomDateTime


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ValidateTokenRequest(BaseModel):
    token: str


class ResetPasswordRequest(ValidateTokenRequest):
    # old_password: str
    new_password: str


class AccountCreateRequest(BaseModel):
    """Schema for creating a new Account."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6, max_length=100)
    type: AccountType = AccountType.USER
    description: str | None = Field(None, min_length=5, max_length=1000)
    files: list["FileCreateRequest"] | None = Field(
        default=None, description="List of files associated with the event"
    )


class AccountUpdateRequest(BaseModel):
    """Schema for updating an existing Account."""

    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = Field(None, description="Valid email address")
    password: str | None = Field(None, min_length=6, max_length=100)
    type: AccountType | None = None
    description: str | None = Field(None, min_length=5, max_length=1000)
    files: list["FileCreateRequest"] | None = Field(
        default=None, description="List of files associated with the account"
    )


# Schema for Account Response
class AccountResponse(BaseModel):
    """Schema for returning Account data."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    email: EmailStr
    type: AccountType
    description: str | None
    creation_date: CustomDateTime
    update_date: CustomDateTime | None
    files: list["FileBasicResponse"]
    businesses: list["BusinessResponse"]
    events: list["EventResponse"]


from .business import BusinessResponse  # noqa: E402
from .event import EventResponse  # noqa: E402
from .file import FileBasicResponse, FileCreateRequest  # noqa: E402
