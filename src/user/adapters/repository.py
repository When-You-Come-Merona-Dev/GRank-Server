from typing import Union
from sqlalchemy.orm import Session
from src.user.services.interfaces.repository import AbstractUserRepository
from src.user.domain.entities.user import User


class SQLAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> None:
        try:
            self.session.add(user)
            self.session.commit()
        except:
            self.session.rollback()
        return

    def get_user_by_github_id(self, github_id: str) -> Union[User, None]:
        user = self.session.query(User).filter(User.github_id == str(github_id)).first()
        return user