from starlette import status
from fastapi.routing import APIRouter
from src.admin.services.unit_of_work import SQLAlchemyUnitOfWork
from src.admin.services import handlers
from src.admin.entrypoints.schema import (
    AdminCreateRequestDto,
    AdminCreateResponseDto,
    AdminLoginRequestDto,
    AdminLoginResponseDto,
)

router = APIRouter()


@router.post(
    "/admin",
    response_model=AdminCreateResponseDto,
    status_code=status.HTTP_201_CREATED,
    tags=["admin"],
)
def add_admin(input_dto: AdminCreateRequestDto) -> AdminCreateResponseDto:
    return handlers.add_admin(input_dto=input_dto, uow=SQLAlchemyUnitOfWork())


@router.post(
    "/admin/login",
    response_model=AdminLoginResponseDto,
    status_code=status.HTTP_200_OK,
    tags=["admin"],
)
def login_admin(input_dto: AdminLoginRequestDto) -> AdminLoginResponseDto:
    return handlers.admin_login(input_dto=input_dto, uow=SQLAlchemyUnitOfWork())