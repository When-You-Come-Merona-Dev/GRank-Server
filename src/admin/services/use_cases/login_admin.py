from fastapi import HTTPException
from src.admin.entrypoints.schema import AdminLoginRequestDto, AdminLoginResponseDto
from src.admin.services.interfaces.repository import AbstractAdminRepository
from src.utils.hasher import check_password
from src.utils.token_handlers import jwt_payload_handler, jwt_encode_handler


class AdminLoginUserCase:
    def __init__(self, repo: AbstractAdminRepository):
        self.repo = repo

    def execute(self, input_dto: AdminLoginRequestDto) -> AdminLoginResponseDto:
        # 존재하는 유저인지 확인
        admin = self.repo.get_admin_by_username(username=input_dto.username)
        if not admin:
            raise HTTPException(status_code=400, detail="Can't login with recieved credentials")

        # 비밀번호 맞는지 확인
        if not check_password(input_dto.password, admin.password):
            raise HTTPException(status_code=400, detail="Can't login with recieved credentials")

        # 토큰 발급
        payload = jwt_payload_handler(user=admin)
        token = jwt_encode_handler(payload=payload)

        output_dto = AdminLoginResponseDto(token=token)
        return output_dto