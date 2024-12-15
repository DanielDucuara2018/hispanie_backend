from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from hispanie.schema import AccountCreateRequest, AccountResponse, AccountUpdateRequest, Token

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
# TODO create a infinite token to get all events and accounts (artists) from frontend
# TODO Implement the refresh_token_id
# TODO Implement rate limiting for sensitive endpoints like /token to prevent brute-force attacks.
# TODO Use Pydantic's advanced validation to enforce business rules, such as password complexity.
# TODO Consider creating a separate set of admin endpoints under a different prefix (e.g., /admin/accounts) for better organization.
# TODO Add logging statements to capture important actions like user authentication and account creation.
@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    expiration_time: Annotated[
        int, Query(description="Set a value in minutes")
    ] = ACCESS_TOKEN_EXPIRE_MINUTES,
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

    expiration_date = generate_expiration_time(delta=expiration_time)
    access_token = create_access_token(
        data={"sub": account.username},
        expiration_date=expiration_date,
    )

    response = JSONResponse(
        content=Token(
            access_token=access_token,
            token_type="bearer",
            token_expiration_date=expiration_date,
        ).model_dump(exclude_none=True)
    )
    response.set_cookie(
        key="sessionid",
        value=refresh_token_id or "random_generated_id",  # TODO Replace with proper logic
        expires=expiration_date,
        httponly=True,
    )
    return response


@router.post("/", response_model=AccountResponse)
async def create(account_data: AccountCreateRequest) -> AccountResponse:
    """
    Create a new account with the provided data.
    """
    try:
        return create_account(account_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating account: {e}"
        )


# TODO add maybe a filter to get artists, users, and admin ?
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
# TODO Use a separate endpoint for password updates to enhance security. Necessary ?
@router.put("/", response_model=AccountResponse)
async def update(
    account_data: AccountUpdateRequest,
    current_account: AccountResponse = Depends(get_current_account),
) -> AccountResponse:
    """
    Update the current account with the provided data.
    """
    try:
        return update_account(current_account.id, account_data)
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
