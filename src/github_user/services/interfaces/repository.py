import abc
from typing import Union, List
from src.github_user.domain.entities.github_user import GithubUser


class AbstractGithubUserRepository(abc.ABC):
    @abc.abstractmethod
    def create_github_user(self, github_user: GithubUser) -> None:
        pass

    @abc.abstractmethod
    def get_github_user_by_username(self, username: str) -> Union[GithubUser, None]:
        pass

    @abc.abstractmethod
    def get_user_by_github_id(self, github_id:str) -> Union[GithubUser, None]:
        pass

    @abc.abstractmethod
    def list_github_user(
        self, filters: dict = {}, page: int = None, per_page: int = None, order_by_field: str = None
    ) -> List[GithubUser]:
        pass

    @abc.abstractmethod
    def approve_github_user(self, github_user: GithubUser) -> GithubUser:
        pass

    @abc.abstractmethod
    def renew_avatar_url(self, github_user: GithubUser, avatar_url: str) -> GithubUser:
        pass

    @abc.abstractmethod
    def renew_commit_count(self, github_user: GithubUser, commit_count: int) -> GithubUser:
        pass