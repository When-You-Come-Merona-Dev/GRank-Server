from typing import Union, List
from sqlalchemy.orm import Session
from src.github_user.domain.entities.github_user import GithubUser
from src.github_user.services.interfaces.repository import AbstractGithubUserRepository


def get_order_by_field_by_str(model_cls, order_by_field: str):
    field = None
    if order_by_field[0] == "-":
        if hasattr(model_cls, order_by_field[1:]):
            field = getattr(model_cls, order_by_field[1:]).desc()
    else:
        if hasattr(model_cls, order_by_field):
            field = getattr(model_cls, order_by_field).asc()
    return field


class GithubUserRepository(AbstractGithubUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_github_user(self, github_user: GithubUser) -> None:
        try:
            self.session.add(github_user)
            self.session.commit()
        except:
            self.session.rollback()
            raise

    def get_github_user_by_username(self, username: str) -> Union[GithubUser, None]:
        github_user = self.session.query(GithubUser).filter(GithubUser.username == username).first()
        return github_user

    def list_github_user(
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

    def approve_github_user(self, github_user: GithubUser) -> GithubUser:
        try:
            github_user.is_approved = True
            self.session.commit()
        except:
            self.session.rollback()
            raise

        return github_user

    def renew_avatar_url(self, github_user: GithubUser, avatar_url: str) -> GithubUser:
        try:
            github_user.avatar_url = avatar_url
            self.session.commit()
        except:
            self.session.rollback()
            raise

        return github_user

    def renew_commit_count(self, github_user: GithubUser, commit_count: int) -> GithubUser:
        try:
            github_user.commit_count = commit_count
            self.session.commit()
        except:
            self.session.rollback()
            raise

        return github_user
