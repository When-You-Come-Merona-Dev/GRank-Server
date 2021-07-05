import abc
from typing import Union
from src.user.domain.entities.user import User


class AbstractUserRepository:
    @abc.abstractmethod
    def create_user(self, user: User) -> None:
        pass

    @abc.abstractmethod
    def get_user_by_github_id(self, github_id: str) -> Union[User, None]:
        pass