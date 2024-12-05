from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from hispanie.schema import AccountCreateUpdateRequest, AccountResponse, Token

from ...action import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_account,
    create_access_token,
    create_account,
    delete_account,
    generate_expiration_time,
    get_current_account,
    read_account,
    update_account,
)
from ...model.account import AccountType

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
)


# Utility functions
def ensure_admin_privileges(current_account: AccountResponse) -> None:
    """Raise an HTTP exception if the current user is not an admin."""
    if current_account.type != AccountType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You have not enough privileges",
        )


# Endpoint Definitions
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    refresh_token_id: str | None = Cookie(None),
) -> JSONResponse:
    """
    Authenticate a user and return an access token.
    """
    account = authenticate_account(form_data.username, form_data.password)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expiration_time = generate_expiration_time(delta=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": account.username},
        expiration_time=expiration_time,
    )

    response = JSONResponse(
        content=Token(
            access_token=access_token,
            token_type="bearer",
            token_expiration=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ).dict()
    )
    response.set_cookie(
        key="sessionid",
        value=refresh_token_id or "random_generated_id",  # TODO Replace with proper logic
        expires=expiration_time,
        httponly=True,
    )
    return response


@router.post("/", response_model=AccountResponse)
async def create(account_data: AccountCreateUpdateRequest) -> AccountResponse:
    """
    Create a new account with the provided data.
    """
    try:
        return create_account(account_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating account: {e}"
        )


@router.get("/", response_model=AccountResponse | list[AccountResponse])
async def read(
    current_account: AccountResponse = Depends(get_current_account),
    show_all: Annotated[bool, Query(description="Set to true to list all users if admin")] = False,
) -> AccountResponse | list[AccountResponse]:
    """
    Get current user data or list all users if admin.
    """
    if show_all:
        ensure_admin_privileges(current_account)
        return read_account()  # Replace with the method to fetch all users

    return current_account


# TODO check AccountCreateUpdateRequest because it could overide everything
@router.put("/", response_model=AccountResponse)
async def update(
    account_request: AccountCreateUpdateRequest,
    current_account: AccountResponse = Depends(get_current_account),
) -> AccountResponse:
    """
    Update the current account with the provided data.
    """
    try:
        return update_account(current_account.id, account_request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating account: {e}"
        )


@router.delete("/", response_model=AccountResponse)
async def delete(
    current_account: AccountResponse = Depends(get_current_account),
) -> AccountResponse:
    """
    Delete the current account.
    """
    try:
        return delete_account(current_account.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error deleting account: {e}"
        )
