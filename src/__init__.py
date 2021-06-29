from fastapi import FastAPI
from src.config import CONFIG
from fastapi.middleware.cors import CORSMiddleware
from src.infra.db.mapper import start_mappers


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


def init_orm():
    start_mappers()


def init_router(app: FastAPI):
    from src.github_user.entrypoints.api import router as github_user_router
    from src.admin.entrypoints.api import router as admin_router

    for router in [github_user_router, admin_router]:
        app.include_router(router)


def create_app() -> FastAPI:
    app = FastAPI(docs_url=None if CONFIG.API_ENV == "production" else "/docs")
    init_router(app)
    init_middleware(app)
    init_orm()
    return app
