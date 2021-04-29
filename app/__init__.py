from fastapi import FastAPI
from core.config import config


def create_app() -> FastAPI:
    app = FastAPI(docs_url=None if config.API_ENV == "production" else "/docs")
    return app


app = create_app