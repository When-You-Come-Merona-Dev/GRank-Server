from typing import Union, List
from sqlalchemy.orm import Session
from src.domain.entities.github_user import GithubUser
from src.services.interfaces.repositories.github_user import AbstractGithubUserRepository


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
        order_by = self.order_by_parser(order_by_field)
        github_users = (
            self.session.query(GithubUser)
            .filter_by(**filters)
            .order_by(order_by)
            .limit(per_page)
            .offset(page * per_page)
        )
        return github_users

    def renew_commit_count(self, commit_count) -> None:
        return None

    def order_by_parser(self, order_by_field):
        return None