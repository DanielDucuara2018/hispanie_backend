import logging
from datetime import datetime, timedelta, timezone

from fastapi import BackgroundTasks, Depends, HTTPException, status
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from itsdangerous import URLSafeTimedSerializer
from jose import JWTError, jwt

from ..config import Config
from ..model import Account, AccountType
from ..schema import AccountCreateRequest, AccountUpdateRequest
from ..utils import OAuth2PasswordBearerWithCookie, check_password_hash

logger = logging.getLogger(__name__)

# to get a string like this run:
# openssl rand -hex 32 TODO Store better these variables

EMAIL_CONFIG = ConnectionConfig(
    MAIL_USERNAME=Config.email.username,
    MAIL_PASSWORD=Config.email.password,
    MAIL_FROM=Config.email.address,
    MAIL_PORT=int(Config.email.port),
    MAIL_SERVER=Config.email.server,
    MAIL_FROM_NAME=Config.email.name,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
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
    background_tasks.add_task(send_reset_email, account.email, reset_token)
    logger.info("Preparing email for account %s to email %s", account.id, account.email)


def handle_reset_password(token: str, old_password: str, new_password: str) -> Account:
    logger.info("Reseting password")
    email = verify_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    accounts = read(email=email)
    if not accounts:
        raise HTTPException(status_code=404, detail="account not found")

    account = accounts[0]
    account = authenticate_account(account.username, old_password)

    result = account.update(password=new_password)
    logger.info("Reseted password for account %s", result.id)


async def send_reset_email(email: str, token: str) -> None:
    logger.info("Sending email to %s", email)
    reset_url = f"{Config.email.frontend_url}/reset-password?token={token}"
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body=f"Please click the following link to reset your password: {reset_url}",
        subtype="html",
    )
    fm = FastMail(EMAIL_CONFIG)
    await fm.send_message(message)
    logger.info("Email sent to %s", email)


def create_reset_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(Config.email.secret_key)
    return serializer.dumps(email, salt=Config.email.security_password_salt)


def verify_reset_token(token: str, expiration: int = 3600) -> str | None:
    serializer = URLSafeTimedSerializer(Config.email.secret_key)
    try:
        return serializer.loads(token, salt=Config.email.security_password_salt, max_age=expiration)
    except Exception:
        return None
