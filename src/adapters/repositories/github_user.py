from typing import Union, List
from sqlalchemy.orm import Session
from src.domain.entities.github_user import GithubUser
from src.services.interfaces.repositories.github_user import AbstractGithubUserRepository


def get_order_by_field_by_str(model_cls, order_by_field: str):
    if order_by_field[0] == "-":
        field = getattr(model_cls, order_by_field[1:]).desc()
    else:
        field = getattr(model_cls, order_by_field).asc()
    return field


class GithubUserRepository(AbstractGithubUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_github_user(self, github_user: GithubUser) -> None:
        self.session.add(github_user)
        self.session.commit()

    def get_github_user_by_username(self, username: str) -> Union[GithubUser, None]:
        github_user = self.session.query(GithubUser).filter(GithubUser.username == username).first()
        return github_user

    def list_github_user(
        self,
        filters: dict,
        page: int,
        per_page: int,
        order_by_field: str,
    ) -> List[GithubUser]:

        if page == None or per_page == None:
            offset = None
        else:
            offset = (page - 1) * per_page

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

    def renew_commit_count(self, commit_count) -> None:
        return None
