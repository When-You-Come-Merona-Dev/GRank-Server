import abc


class AbstractExternalAPIClient(abc.ABC):
    @abc.abstractmethod
    def get_commit_count_from_username(self, username: str) -> int:
        pass

    @abc.abstractmethod
    def get_avatar_url_from_username(self, username: str) -> str:
        pass
