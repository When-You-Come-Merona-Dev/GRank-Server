from starlette.requests import Request
from starlette.responses import JSONResponse
from src.infra.db.mapper import start_mappers
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.middlewares.authentication import AuthenticationMiddleware, JWTAuthenticationBackend
from src.config import CONFIG
from src.utils.exceptions import APIException


def init_middleware(app: FastAPI):
    app.add_middleware(AuthenticationMiddleware, backend=JWTAuthenticationBackend())

    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(APIException)
    async def api_exception_handler(request: Request, ex: APIException):
        return JSONResponse(status_code=ex.status_code, content={"error": ex.detail})

    @app.exception_handler(Exception)
    async def internal_exception_handler(request: Request, ex: Exception):
        return JSONResponse(status_code=500, content={"error": str(ex)})


def init_orm():
    start_mappers()


def init_router(app: FastAPI):
    app.mount("/static", StaticFiles(directory="static"), name="static")

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
