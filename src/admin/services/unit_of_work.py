import abc
from src.admin.services.interfaces.repository import AbstractRepository
from src.admin.adapters.repository import SQLAlchemyRepository
from src.infra.db.session import sqlalchemy_session_factory

DEFAULT_SESSION_FACTIRY = sqlalchemy_session_factory


class AbstractUnitOfWork(abc.ABC):
    admins: AbstractRepository

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTIRY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.admins = SQLAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()