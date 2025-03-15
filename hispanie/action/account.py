import logging
from datetime import datetime, timedelta, timezone
from typing import overload

from fastapi import BackgroundTasks, Depends, HTTPException, status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from itsdangerous import URLSafeTimedSerializer
from jose import JWTError, jwt
from pydantic import SecretStr

from ..config import Config
from ..model import Account, AccountType, File, ResetToken
from ..schema import AccountCreateRequest, AccountUpdateRequest
from ..utils import OAuth2PasswordBearerWithCookie, check_password_hash, handle_update_files

logger = logging.getLogger(__name__)

# to get a string like this run:
# openssl rand -hex 32 TODO Store better these variables

EMAIL_CONFIG = ConnectionConfig(
    MAIL_USERNAME=Config.email.username,
    MAIL_PASSWORD=SecretStr(Config.email.password),
    MAIL_FROM=Config.email.address,
    MAIL_PORT=int(Config.email.port),
    MAIL_SERVER=Config.email.server,
    MAIL_FROM_NAME=Config.email.name,
    MAIL_STARTTLS=bool(int(Config.email.start_tls)),
    MAIL_SSL_TLS=bool(int(Config.email.ssl_tls)),
    USE_CREDENTIALS=bool(int(Config.email.credentials)),
    VALIDATE_CERTS=bool(int(Config.email.validate_certs)),
)

CREDENTIAL_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/accounts/public/login")


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


@overload
def read(account_id: str) -> Account: ...
@overload
def read(**kwargs) -> list[Account]: ...
def read(account_id: str | None = None, **kwargs) -> Account | list[Account]:
    if account_id:
        logger.info("Reading account: %s", account_id)
        account = Account.get(id=account_id)
        logger.info("Data found for account %s", account.id)
        return account
    else:
        logger.info("Reading all accounts with filters %s", kwargs)
        accounts = Account.find(**kwargs)
        logger.info("Data found for account %s", [ac.id for ac in accounts])
        return accounts


# update account


def update(account_id: str, account_data: AccountUpdateRequest) -> Account:
    logger.info("Updating %s with data %s", account_id, account_data)
    account = Account.get(id=account_id)
    data = account_data.model_dump(exclude_none=True)
    if files := data.pop("files", []):
        data["files"] = handle_update_files(files, File)
    if old_password := data.pop("old_password", ""):
        authenticate_account(account.username, old_password)
    result = account.update(**data)
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


# create account access token


def create_access_token(data: dict, expiration_date: datetime) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": expiration_date})
    return jwt.encode(to_encode, Config.jwt.secret_key, algorithm=Config.jwt.algorithm)


def generate_expiration_time(delta: int) -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=delta)


# get account for authentification


async def check_account_session(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, Config.jwt.secret_key, algorithms=[Config.jwt.algorithm])
    except JWTError:
        raise CREDENTIAL_EXCEPTION

    if not (username := payload.get("sub")):
        raise CREDENTIAL_EXCEPTION

    return username


async def get_current_account(token: str = Depends(oauth2_scheme)) -> Account:
    accounts = read(username=await check_account_session(token))
    if not accounts:
        raise CREDENTIAL_EXCEPTION
    return accounts[0]


# handle password forgotten


def handle_forgotten_password(email: str, background_tasks: BackgroundTasks) -> None:
    logger.info("Processing forgotten password request")
    accounts = read(email=email)
    if not accounts:
        raise HTTPException(status_code=404, detail="account not found")

    account = accounts[0]
    reset_token = create_reset_token(account.email)
    background_tasks.add_task(send_reset_email, account, reset_token)
    logger.info("Preparing email for account %s to email %s", account.id, account.email)


def handle_reset_password(token: str, new_password: str) -> None:
    logger.info("Reseting password")

    is_used = is_reset_token_used(token)
    if is_used:
        raise HTTPException(status_code=400, detail="This token was already used")

    email = verify_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    accounts = read(email=email)
    if not accounts:
        raise HTTPException(status_code=404, detail="account not found")

    result = accounts[0].update(password=new_password)
    logger.info("Reseted password for account %s", result.id)
    set_reset_token_as_used(token)


async def send_reset_email(account: Account, token: str) -> None:
    logger.info("Sending email to %s", account.email)
    reset_url = f"{Config.email.frontend_url}/reset_password?token={token}"
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[account.email],
        body=f"Please click the following link to reset your password: {reset_url}",
        subtype=MessageType.html,
    )
    fm = FastMail(EMAIL_CONFIG)
    await fm.send_message(message)
    logger.info("Email sent to %s", account.email)
    save_reset_token(account, token)


def save_reset_token(account: Account, token: str) -> None:
    [reset_token.update(used=True) for reset_token in account.reset_tokens]
    logger.info("Saving reset token in DB")
    ResetToken(id=token, account=account).create()
    logger.info("Saved reset token in DB")


def is_reset_token_used(token: str) -> bool:
    logger.info("Validating if reset token was used")
    reset_token = ResetToken.get(id=token)
    logger.info("Reset token status used = %s", reset_token.used)
    return reset_token.used


def set_reset_token_as_used(token: str) -> None:
    logger.info("Set reset token as used")
    reset_token = ResetToken.get(id=token).update(used=True)
    logger.info("Reset token status used = %s", reset_token.used)


def create_reset_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(Config.email.secret_key)
    return serializer.dumps(email, salt=Config.email.security_password_salt)


def verify_reset_token(token: str, expiration: int = 3600) -> str | None:
    serializer = URLSafeTimedSerializer(Config.email.secret_key)
    try:
        return serializer.loads(token, salt=Config.email.security_password_salt, max_age=expiration)
    except Exception:
        return None
