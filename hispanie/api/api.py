import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..db import initialize
from .routers.account import router as account_router

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# def import_all_models(directory: Path):
#     """Import all modules in the given directory."""

#     for file in directory.glob("*.py"):
#         logger.info(file)
#         if "__init__.py" not in file.name and file.suffix == ".py":
#             module_name = f"hispanie.model.{file.stem}"
#             logger.info(module_name)
#             spec = importlib.util.spec_from_file_location(module_name, file)
#             module = importlib.util.module_from_spec(spec)
#             spec.loader.exec_module(module)

# import_all_models(Path(__file__).parent.parent.resolve().joinpath("model"))

initialize(True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_router)


@app.get("/")
async def root():
    return {"message": "Welcome to hispanie app"}
