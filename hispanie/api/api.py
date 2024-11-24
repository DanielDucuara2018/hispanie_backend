import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from hispanie.api.routers.user import router as user_router
from hispanie.db import initialize

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

# app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Welcome to hispanie app"}
