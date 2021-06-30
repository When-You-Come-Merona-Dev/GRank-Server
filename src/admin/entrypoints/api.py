from sqlalchemy.orm.session import Session
from starlette import status
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from src.admin.services.use_cases.add_admin import AdminAddUserCase
from src.admin.services.use_cases.login_admin import AdminLoginUserCase
from src.admin.adapters.repository import AdminRepository
from src.infra.db.session import get_session
from src.admin.entrypoints.schema import (
    AdminCreateRequestDto,
    AdminCreateResponseDto,
    AdminLoginRequestDto,
    AdminLoginResponseDto,
)

router = APIRouter()
security = HTTPBearer()


@router.post("/admin", response_model=AdminCreateResponseDto, status_code=status.HTTP_201_CREATED)
def add_admin(
    admin: AdminCreateRequestDto, session: Session = Depends(get_session)
) -> AdminCreateResponseDto:
    repo = AdminRepository(session)
    use_case = AdminAddUserCase(repo=repo)

    output_dto = use_case.execute(admin)
    return output_dto


@router.post("/admin/login", response_model=AdminLoginResponseDto, status_code=status.HTTP_200_OK)
def login_admin(
    admin: AdminLoginRequestDto, session: Session = Depends(get_session)
) -> AdminLoginResponseDto:
    repo = AdminRepository(session)
    use_case = AdminLoginUserCase(repo=repo)

    output_dto = use_case.execute(admin)
    return output_dto