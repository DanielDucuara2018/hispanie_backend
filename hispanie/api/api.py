import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..db import initialize
from .routers.account import router as account_router
from .routers.event import router as event_router

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

initialize(True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_router, prefix="/api/v1")
app.include_router(event_router, prefix="/api/v1")


@app.get("/api/v1")
async def root():
    return {"message": "Welcome to hispanie app"}
