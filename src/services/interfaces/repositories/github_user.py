import abc
from src.domain.entities.github_user import GithubUser


class AbstractGithubUserRepository(abc.ABC):
    @abc.abstractmethod
    def create_github_user(self, github_user: GithubUser) -> GithubUser:
        pass

    @abc.abstractmethod
    def renew_one_commit_count(self):
        pass

    @abc.abstractmethod
    def renew_all_commit_count(self):
        pass
