import abc
from typing import Union, List
from src.domain.entities.github_user import GithubUser


class AbstractGithubUserRepository(abc.ABC):
    @abc.abstractmethod
    def create_github_user(self, github_user: GithubUser) -> None:
        pass

    @abc.abstractmethod
    def get_github_user_by_username(self, username: str) -> Union[GithubUser, None]:
        pass

    @abc.abstractmethod
    def list_github_user(
        self, filters: dict, page: int, per_page: int, order_by_field: str
    ) -> List[GithubUser]:
        pass

    @abc.abstractmethod
    def renew_commit_count(self, commit_count) -> None:
        pass