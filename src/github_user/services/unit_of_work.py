import abc
from src.github_user.services.interfaces.repository import AbstractRepository
from src.github_user.adapters.repository import SQLAlchemyRepository
from src.config import CONFIG


class AbstractUnitOfWork(abc.ABC):
    github_users: AbstractRepository

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=CONFIG.DEFAULT_SESSION_FACTIRY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.github_users = SQLAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()