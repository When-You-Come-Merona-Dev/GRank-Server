from sqlalchemy.orm import Session
from src.admin.services.interfaces.repository import AbstractRepository
from src.admin.domain.entities.admin import Admin, AdminCertificationCode


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def add(self, admin: Admin) -> None:
        self.session.add(admin)

    def get_by_username(self, username: str) -> Admin:
        return self.session.query(Admin).filter(Admin.username == username).first()

    def get_admin_certification_code_by_code(self, code: str) -> AdminCertificationCode:
        return (
            self.session.query(AdminCertificationCode)
            .filter(AdminCertificationCode.code == code)
            .first()
        )

    def delete_admin_certification_code(
        self, admin_certification_code: AdminCertificationCode
    ) -> None:
        self.session.expunge(admin_certification_code)