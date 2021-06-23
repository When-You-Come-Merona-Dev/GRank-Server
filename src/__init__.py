from fastapi import FastAPI
from core.config import config
from fastapi.middleware.cors import CORSMiddleware


def init_middleware(app: FastAPI):
    origins = [
        "http://localhost",
        "http://localhost:3052",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_router(app: FastAPI):
    from src.entrypoints.api import router as github_user_router

    app.include_router(github_user_router)


def create_app() -> FastAPI:
    app = FastAPI(docs_url=None if config.API_ENV == "production" else "/docs")
    init_router(app)
    init_middleware(app)


app = create_app()