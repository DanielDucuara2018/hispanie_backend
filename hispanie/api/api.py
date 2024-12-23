import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..db import initialize
from .routers.account import router as account_router
from .routers.business import router as business_router
from .routers.event import router as event_router

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

API_PREFIX = "/api/v1"

logger = logging.getLogger(__name__)

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
app.include_router(event_router, prefix=API_PREFIX)
app.include_router(business_router, prefix=API_PREFIX)


@app.get("/api/v1")
async def root():
    return {"message": "Welcome to hispanie app"}
