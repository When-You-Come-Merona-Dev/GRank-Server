from sqlalchemy.orm import Session
from src.admin.services.interfaces.repository import AbstractAdminRepository
from src.admin.domain.entities.admin import Admin, AdminCertificationCode


class AdminRepository(AbstractAdminRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_admin(self, admin: Admin) -> None:
        try:
            self.session.add(admin)
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def get_admin_by_username(self, username: str) -> Admin:
        admin = self.session.query(Admin).filter(Admin.username == username).first()
        return admin

    def get_admin_certification_code_by_code(self, code: str) -> AdminCertificationCode:
        admin_certification_code = (
            self.session.query(AdminCertificationCode)
            .filter(AdminCertificationCode.code == code)
            .first()
        )
        return admin_certification_code

    def delete_admin_certification_code(
        self, admin_certification_code: AdminCertificationCode
    ) -> None:
        try:
            self.session.delete(admin_certification_code)
            self.session.commit()
        except:
            self.session.rollback()
            raise