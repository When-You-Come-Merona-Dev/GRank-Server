from typing import Union, List
from sqlalchemy.orm import Session
from src.github_user.domain.entities.github_user import GithubUser
from src.github_user.services.interfaces.repository import AbstractRepository


def get_order_by_field_by_str(model_cls, order_by_field: str):
    field = None
    if order_by_field[0] == "-":
        if hasattr(model_cls, order_by_field[1:]):
            field = getattr(model_cls, order_by_field[1:]).desc()
    else:
        if hasattr(model_cls, order_by_field):
            field = getattr(model_cls, order_by_field).asc()
    return field


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    # ===== CREATE =====
    def add(self, github_user: GithubUser) -> None:
        self.session.add(github_user)

    # ===== READ =====
    def get_by_username(self, username: str) -> Union[GithubUser, None]:
        return self.session.query(GithubUser).filter(GithubUser.username == username).first()

    def get_by_github_id(self, github_id: str) -> Union[GithubUser, None]:
        return self.session.query(GithubUser).filter(GithubUser.github_id == str(github_id)).first()

    def list(
        self, filters: dict = {}, page: int = None, per_page: int = None, order_by_field: str = None
    ) -> List[GithubUser]:

        if page == None or per_page == None:
            offset = None
        else:
            offset = (page - 1) * per_page

        if order_by_field == None:
            order_by = None
        else:
            order_by = get_order_by_field_by_str(GithubUser, order_by_field)

        github_users = (
            self.session.query(GithubUser)
            .filter_by(**filters)
            .order_by(order_by)
            .limit(per_page)
            .offset(offset)
            .all()
        )
        return github_users

    # ===== DELETE =====
    def delete(self, github_user: GithubUser) -> None:
        self.session.delete(github_user)
        return
