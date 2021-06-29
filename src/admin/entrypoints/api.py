from src.admin.services.use_cases.add_admin import AdminAddUserCase
from src.admin.adapters.repository import AdminRepository
from src.infra.db.session import get_session
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from src.admin.entrypoints.schema import AdminCreateRequestDto, AdminCreateResponseDto
from fastapi.routing import APIRouter
from starlette import status


router = APIRouter()


@router.post("/admin", response_model=AdminCreateResponseDto, status_code=status.HTTP_201_CREATED)
def add_admin(
    admin: AdminCreateRequestDto, session: Session = Depends(get_session)
) -> AdminCreateResponseDto:
    repo = AdminRepository(session)
    use_case = AdminAddUserCase(repo=repo)

    output_dto = use_case.execute(admin)
    return output_dto
