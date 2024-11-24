from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

# from hispanie.model import User as ModelUser
# from hispanie.schema import UserRequest as SchemaUserRequest

logger = logging.getLogger(__name__)

# to get a string like this run:
# openssl rand -hex 32 TODO Store better these variables
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

# create User


# def create(user: SchemaUserRequest) -> ModelUser:
#     logger.info("Adding new user")
#     result = ModelUser(**dict(user)).create()
#     logger.info("Added new user %s", result.user_id)
#     return result


# delete User


# def delete(user_id: str) -> ModelUser:
#     logger.info("Deleting %s user", user_id)
#     result = ModelUser.get(user_id=user_id).delete()
#     logger.info("Deleted user %s", user_id)
#     return result


# get User


# def read(user_id: Optional[str] = None, **kwargs) -> Union[ModelUser, list[ModelUser]]:
#     if user_id:
#         logger.info("Reading %s data", user_id)
#         result = ModelUser.get(user_id=user_id)
#     else:
#         logger.info("Reading all data")
#         result = ModelUser.find(**kwargs)
#     logger.info("Data found for user %s", user_id)
#     return result


# update User


# def update(
#     user_id: str,
#     data: Optional[SchemaUserRequest] = None,
#     is_admin: Optional[bool] = None,
# ) -> ModelUser:
#     logger.info("Updating %s with data %s", user_id, data or is_admin)
#     user = ModelUser.get(user_id=user_id)
#     if data:
#         result = user.update(**dict(data))
#     else:
#         result = user.update(is_admin=is_admin)
#     logger.info("Updated user %s", user_id)
#     return result


# authenticate User


# def authenticate_user(username: str, password: str) -> Optional[ModelUser]:
#     users = read(username=username)
#     if users and check_password_hash(users[0].password, password):
#         return users[0]
#     return None


def generate_expiration_time(delta: int = 15) -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=delta)


# create User access token


def create_access_token(data: dict, expiration_time: datetime) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": expiration_time})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# get User for authentification


# async def get_current_user(token: str = Depends(oauth2_scheme)) -> ModelUser:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     except JWTError:
#         raise credentials_exception

#     if not (username := payload.get("sub")):
#         raise credentials_exception

#     users = read(username=username)
#     if not users:
#         raise credentials_exception
#     return users[0]
