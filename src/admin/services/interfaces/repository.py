import abc
from src.admin.domain.entities.admin import Admin


class AbstractAdminRepository:
    @abc.abstractmethod
    def create_admin(self, admin: Admin):
        pass