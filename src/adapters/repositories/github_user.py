from typing import Union
from src.services.interfaces.repositories.github_user import AbstractGithubUserRepository
from src.domain.entities.github_user import GithubUser
from sqlalchemy.orm import Session


class GithubUserRepository(AbstractGithubUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_github_user(self, github_user: GithubUser) -> None:
        self.session.add(github_user)
        self.session.commit()

    def get_github_user_by_username(self, username: str) -> Union[GithubUser, None]:
        github_user = self.session.query(GithubUser).filter(GithubUser.username == username).first()
        return github_user

    def renew_one_commit_count(self):
        pass

    def renew_all_commit_count(self):
        pass