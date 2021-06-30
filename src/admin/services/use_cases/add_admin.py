from fastapi import HTTPException
from src.admin.entrypoints.schema import AdminCreateRequestDto, AdminCreateResponseDto
from src.admin.services.interfaces.repository import AbstractAdminRepository
from src.admin.domain.entities.admin import Admin
from src.utils.hasher import hash_password


class AdminAddUserCase:
    def __init__(self, repo: AbstractAdminRepository):
        self.repo = repo

    def execute(self, input_dto: AdminCreateRequestDto) -> AdminCreateResponseDto:
        admin_certification_code = self.repo.get_admin_certification_code_by_code(
            code=input_dto.certification_code
        )
        if not admin_certification_code:
            raise HTTPException(status_code=400, detail="certification code is not available")

        exists_admin = self.repo.get_admin_by_username(input_dto.username)

        if exists_admin:
            raise HTTPException(status_code=400, detail="already exists admin username")

        hashed_password = hash_password(input_dto.password)
        admin = Admin(username=input_dto.username, password=hashed_password)

        self.repo.create_admin(admin)
        self.repo.delete_admin_certification_code(admin_certification_code)

        output_dto = AdminCreateResponseDto(**admin.to_dict())
        return output_dto