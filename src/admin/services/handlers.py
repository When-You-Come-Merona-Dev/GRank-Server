from starlette.exceptions import HTTPException
from src.admin.services.unit_of_work import AbstractUnitOfWork
from src.admin.entrypoints.schema import (
    AdminCreateRequestDto,
    AdminCreateResponseDto,
    AdminLoginRequestDto,
    AdminLoginResponseDto,
)
from src.admin.domain.entities.admin import Admin
from src.utils.hasher import hash_password, check_password
from src.utils.token_handlers import jwt_payload_handler, jwt_encode_handler


def add_admin(input_dto: AdminCreateRequestDto, uow: AbstractUnitOfWork) -> AdminCreateResponseDto:
    with uow:
        admin_certification_code = uow.admins.get_admin_certification_code_by_code(
            code=input_dto.certification_code
        )
        if not admin_certification_code:
            raise HTTPException(status_code=400, detail="certification code is not available")

        exists_admin = uow.admins.get_by_username(input_dto.username)

        if exists_admin:
            raise HTTPException(status_code=400, detail="already exists admin username")

        hashed_password = hash_password(input_dto.password)
        admin = Admin(username=input_dto.username, password=hashed_password)

        uow.admins.add(admin)
        uow.admins.delete_admin_certification_code(admin_certification_code)
        username = admin.username
        uow.commit()

    return AdminCreateResponseDto(username=username)


def admin_login(input_dto: AdminLoginRequestDto, uow: AbstractUnitOfWork) -> AdminLoginResponseDto:
    with uow:
        admin = uow.admins.get_by_username(username=input_dto.username)
        if not admin:
            raise HTTPException(status_code=400, detail="Can't login with recieved credentials")

        if not check_password(input_dto.password, admin.password):
            raise HTTPException(status_code=400, detail="Can't login with recieved credentials")

        payload = jwt_payload_handler(user=admin)
        token = jwt_encode_handler(payload=payload)

    return AdminLoginResponseDto(token=token)