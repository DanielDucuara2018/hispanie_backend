import logging
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from ..config import Config
from ..db import initialize
from ..model import Account, AccountType, Event, EventFrequency
from .routers.account import router as account_router
from .routers.activity import router as activity_router
from .routers.business import router as business_router
from .routers.event import router as event_router
from .routers.file import router as file_router
from .routers.tag import router as tag_router
from .routers.ticket import router as ticket_router

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


API_PREFIX = "/api/v1"

mapping_frequency_days = {
    EventFrequency.DAILY: "days",
    EventFrequency.WEEKLY: "weeks",
    EventFrequency.MONTHLY: "months",
}

initialize(True)

app = FastAPI()

# TODO Limit these to specific origins, methods, and headers to reduce the attack surface.
# TODO If you set allow_credentials=True, you must carefully pair it with restrictive allow_origins settings to avoid exposing sensitive data to untrusted origins.
# example
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["https://example.com", "https://another.com"], # my frontend app
#     allow_credentials=True,
#     allow_methods=["GET", "POST" "PUT", "DELETE"],
#     allow_headers=["Authorization", "Content-Type"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3202"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_router, prefix=API_PREFIX)
app.include_router(activity_router, prefix=API_PREFIX)
app.include_router(business_router, prefix=API_PREFIX)
app.include_router(event_router, prefix=API_PREFIX)
app.include_router(file_router, prefix=API_PREFIX)
app.include_router(tag_router, prefix=API_PREFIX)
app.include_router(ticket_router, prefix=API_PREFIX)


@app.on_event("startup")
async def startup_event():
    logger.info("Creating hispanie admin account")

    account = Account.find(username=Config.account.username)
    if account:
        logger.info("Account %s already exists %s", Config.account.username, account[0].id)
        return

    account = Account(
        username=Config.account.username,
        password=Config.account.password,
        email=Config.account.email,
        phone=Config.account.phone,
        description=Config.account.description,
        type=AccountType.ADMIN,
    ).create()
    logger.info("Account %s was just created with id %s", Config.account.username, account.id)


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # 1 day
async def update_periodic_events() -> None:
    logger.info("Updating periodic events")
    today = datetime.today().replace(tzinfo=timezone.utc)
    for event in Event.find(**{"!frequency": EventFrequency.NONE}):
        if event.end_date > today:
            continue

        timedelta_args = {mapping_frequency_days[event.frequency]: 1}
        event.update(
            start_date=event.start_date + timedelta(**timedelta_args),
            end_date=event.end_date + timedelta(**timedelta_args),
        )

        [
            activity.update(
                start_date=activity.start_date + timedelta(**timedelta_args),
                end_date=activity.end_date + timedelta(**timedelta_args),
            )
            for activity in event.activities
        ]


@app.get(API_PREFIX)
async def root():
    return {"message": "Welcome to hispanie app"}
