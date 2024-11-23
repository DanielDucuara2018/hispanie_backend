from typing import Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from hispanie.actions.user import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    # create,
    create_access_token,
    # delete,
    generate_expiration_time,
    # get_current_user,
    # read,
    # update,
)

# from hispanie.errors import Error
from hispanie.schema.user import Token

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


## Users
## get token
@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    refreshTokenId: Optional[str] = Cookie(None),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expiration_time = generate_expiration_time(delta=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expiration_time=expiration_time,
    )

    response = JSONResponse(
        content=Token(
            access_token=access_token,
            token_type="bearer",
            token_expiry=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ).dict(),
    )

    response.set_cookie(
        key="sessionid",
        value="iskksioskassyidd",  # refreshTokenId,
        expires=expiration_time,
        httponly=True,
    )

    return response


# add new user in database
# @router.post("/")
# async def create_user(user: UserRequest) -> UserResponse:
#     return create(user)


# get user data
# @router.get("/me", response_model=UserResponse)
# async def read_user(
#     current_user: UserResponse = Depends(get_current_user),
# ) -> UserResponse:
#     return current_user


# @router.get("/")
# async def read_users(
#     current_user: UserResponse = Depends(get_current_user),
# ) -> list[UserResponse]:
#     if not current_user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="You have not enough privileges",
#         )
#     return read()


# update user data
# @router.put("/")
# async def update_user(
#     data: UserRequest, current_user: UserResponse = Depends(get_current_user)
# ) -> UserResponse:
#     return update(current_user.user_id, data)


# @router.put("/admin")
# async def declare_admin(
#     user_id: str, current_user: UserResponse = Depends(get_current_user)
# ) -> bool:
#     if not current_user.is_admin:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="You have not enough privileges",
#         )

#     try:
#         return update(user_id, is_admin=True).is_admin
#     except Error as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.reason)


# delete existing user from db
# @router.delete("/")
# async def delete_currency(
#     current_user: UserResponse = Depends(get_current_user),
# ) -> UserResponse:
#     return delete(current_user.user_id)
