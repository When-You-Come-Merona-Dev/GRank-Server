import abc


class AbstractCrawler(abc.ABC):
    @abc.abstractmethod
    def get_commit_count_from_username(self, username):
        pass