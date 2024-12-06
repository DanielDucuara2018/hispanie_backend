from pydantic import BaseModel, EmailStr, Field

from ..model import AccountType


class Token(BaseModel):
    access_token: str
    token_type: str
    token_expiration: int


class AccountCreateRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    type: AccountType = AccountType.USER


class AccountUpdateRequest(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=6, max_length=100)
    type: AccountType | None = None


# Schema for Account Response
class AccountResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    type: AccountType

    class Config:
        from_attributes = True
