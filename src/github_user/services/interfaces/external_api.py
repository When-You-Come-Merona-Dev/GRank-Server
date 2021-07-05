import abc


class AbstractExternalAPIClient(abc.ABC):
    @abc.abstractmethod
    def get_commit_count_from_username(self, username: str) -> int:
        pass

    @abc.abstractmethod
    def get_avatar_url_from_username(self, username: str) -> str:
        pass

    @abc.abstractmethod
    def get_github_oauth_token(self, code) -> str:
        pass

    @abc.abstractmethod
    def get_github_user_info(self, oauth_token) -> str:
        pass