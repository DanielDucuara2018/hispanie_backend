import logging
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from ..model import Account, AccountType
from ..schema import AccountCreateRequest, AccountUpdateRequest
from ..utils import OAuth2PasswordBearerWithCookie, check_password_hash

logger = logging.getLogger(__name__)

# to get a string like this run:
# openssl rand -hex 32 TODO Store better these variables
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

CREDENTIAL_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/accounts/login")


# create account


def create(account_data: AccountCreateRequest) -> Account:
    logger.info("Adding new account")
    account = Account(
        username=account_data.username,
        email=account_data.email,
        type=AccountType(account_data.type),
        password=account_data.password,
    ).create()
    logger.info("Added new account %s", account.id)
    return account


# get account


def read(account_id: str | None = None, **kwargs) -> Account | list[Account]:
    if account_id:
        logger.info("Reading %s data", account_id)
        result = Account.get(id=account_id)
    else:
        logger.info("Reading all data")
        result = Account.find(**kwargs)
    logger.info("Data found for account %s", account_id or kwargs)
    return result


# update account


def update(account_id: str, account_data: AccountUpdateRequest) -> Account:
    logger.info("Updating %s with data %s", account_id, account_data)
    account = Account.get(id=account_id)
    result = account.update(**account_data.model_dump(exclude_none=True))
    logger.info("Updated account %s", account_id)
    return result


# delete account


def delete(account_id: str) -> Account:
    logger.info("Deleting %s account", account_id)
    result = Account.get(id=account_id).delete()
    logger.info("Deleted account %s", account_id)
    return result


# authenticate account


def authenticate_account(username: str, password: str) -> Account | None:
    accounts = read(username=username)
    if accounts and check_password_hash(accounts[0].password, password):
        return accounts[0]
    return None


def generate_expiration_time(delta: int) -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=delta)


# create account access token


def create_access_token(data: dict, expiration_date: datetime) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": expiration_date})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# get account for authentification


def check_account_session(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise CREDENTIAL_EXCEPTION

    if not (username := payload.get("sub")):
        raise CREDENTIAL_EXCEPTION

    return username


async def get_current_account(token: str = Depends(oauth2_scheme)) -> Account:
    users = read(username=check_account_session(token))
    if not users:
        raise CREDENTIAL_EXCEPTION
    return users[0]
