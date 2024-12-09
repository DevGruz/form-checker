from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import config
from app.core.db import mongo_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    if config.INIT_DATA_IN_DATABASE:
        await mongo_settings.init_db("data/templates.json")
    yield
    mongo_settings.client_close()


app = FastAPI(
    title=config.PROJECT_NAME,
    lifespan=lifespan,
)

app.include_router(api_router)
