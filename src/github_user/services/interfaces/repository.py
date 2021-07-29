import abc
from typing import Union, List
from src.github_user.domain.entities.github_user import GithubUser


class AbstractRepository(abc.ABC):
    # ===== CREATE =====
    @abc.abstractmethod
    def add(self, github_user: GithubUser) -> None:
        pass

    # ===== READ =====
    @abc.abstractmethod
    def get_by_username(self, username: str) -> Union[GithubUser, None]:
        pass

    @abc.abstractmethod
    def get_by_github_id(self, github_id: str) -> Union[GithubUser, None]:
        pass

    @abc.abstractmethod
    def list(
        self, filters: dict = {}, page: int = None, per_page: int = None, order_by_field: str = None
    ) -> List[GithubUser]:
        pass

    # ===== DELETE =====
    @abc.abstractmethod
    def delete(self, github_user: GithubUser) -> None:
        pass