import abc
from src.admin.domain.entities.admin import Admin, AdminCertificationCode


class AbstractRepository:
    @abc.abstractmethod
    def add(self, admin: Admin) -> None:
        pass

    @abc.abstractmethod
    def get_by_username(self, username: str) -> Admin:
        pass

    @abc.abstractmethod
    def get_admin_certification_code_by_code(self, code: str) -> AdminCertificationCode:
        pass

    @abc.abstractmethod
    def delete_admin_certification_code(
        self, admin_certification_code: AdminCertificationCode
    ) -> None:
        pass