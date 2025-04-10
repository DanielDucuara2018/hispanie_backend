from typing import Annotated

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Cookie,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from hispanie.schema import (
    AccountCreateRequest,
    AccountResponse,
    AccountUpdateRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    Token,
    ValidateTokenRequest,
)

from ...action import (
    authenticate_account,
    create_access_token,
    create_account,
    delete_account,
    generate_expiration_time,
    get_current_account,
    handle_forgotten_password,
    handle_reset_password,
    is_reset_token_used,
    read_accounts,
    update_account,
)
from ...config import Config
from ...model.account import Account, AccountType
from ...utils import TOKEN_KEY_NAME

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
@router.post("/public/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    expiration_time: Annotated[int, Query(description="Set a value in minutes")] = int(
        Config.jwt.access_token_expire_minutes
    ),
    refresh_token_id: str | None = Cookie(None),
) -> JSONResponse:
    """Authenticate a account and return an access token."""
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
        ).model_dump(exclude_none=True),
        status_code=status.HTTP_200_OK,
    )

    response.set_cookie(
        key=TOKEN_KEY_NAME,
        value=f"Bearer {access_token}",
        expires=expiration_date,
        httponly=True,
        secure=False,  # Set True in production with HTTPS
        samesite=None,
    )

    return response


# TODO add token account validation
@router.post("/private/logout")
async def logout(response: Response, _: None = Depends(get_current_account)) -> None:
    """Log out an account and delete the cookies info."""
    response.delete_cookie(key=TOKEN_KEY_NAME)


@router.post("/public/validate_reset_token")
async def validate_reset_token(result: ValidateTokenRequest) -> bool:
    return is_reset_token_used(result.token)


@router.post("/public/forgot_password")
async def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
) -> None:
    """Handle forgotten password request for a given account."""
    try:
        handle_forgotten_password(request.email, background_tasks)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error handling forgotten password: {e}",
        )


@router.post("/public/reset_password")
async def reset_password(
    request: ResetPasswordRequest,
) -> None:
    """Handle reset password request for a given account."""
    try:
        handle_reset_password(**request.model_dump(exclude_none=True))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error handling forgotten password: {e}",
        )


@router.post("/public/create", response_model=AccountResponse)
async def create(
    account_data: AccountCreateRequest,  # _: None = Depends(get_current_account)
) -> Account:
    """Create a new account with the provided data."""
    try:
        return create_account(account_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error creating account: {e}"
        )


# TODO add maybe a filter to get artists, users, and admin ?
@router.get("/private/read", response_model=AccountResponse | list[AccountResponse])
async def read(
    current_account: AccountResponse = Depends(get_current_account),
    show_all: Annotated[bool, Query(description="Set to true to list all users if admin")] = False,
) -> AccountResponse | list[Account]:
    """Get current user data or list all users if admin."""
    if show_all:
        ensure_admin_privileges(current_account)
        return read_accounts()  # Replace with the method to fetch all users

    return current_account


# TODO check AccountCreateUpdateRequest because it could overide everything
# TODO Use a separate endpoint for password updates to enhance security. Necessary ?
@router.put("/private/update", response_model=AccountResponse)
async def update(
    account_data: AccountUpdateRequest,
    current_account: AccountResponse = Depends(get_current_account),
) -> Account:
    """Update the current account with the provided data."""
    try:
        return update_account(current_account.id, account_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error updating account: {e}"
        )


@router.delete("/private/delete", response_model=AccountResponse)
async def delete(
    current_account: AccountResponse = Depends(get_current_account),
) -> Account:
    """Delete the current account."""
    try:
        return delete_account(current_account.id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error deleting account: {e}"
        )
