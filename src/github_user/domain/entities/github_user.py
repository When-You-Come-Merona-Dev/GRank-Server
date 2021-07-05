from src.github_user.domain.entities.group import Group
from src.config import CONFIG


class GithubUser:
    def __init__(self, username: str):
        self.id = None
        self.username = username
        self.avatar_url = CONFIG.DOMAIN + "/static/images/default_github_user_avatar.png"
        self.commit_count = 0
        self.is_approved = False
        self._groups = set()
        self._social_authentication_id = None
        self.created_at = None
        self.updated_at = None

    @property
    def groups(self):
        return self._groups

    @property
    def social_authentication_id(self):
        return self._social_authentication_id

    def join_group(self, group: Group):
        self._groups.add(group)

    def leave_group(self, group: Group):
        if group in self._groups:
            self._groups.remove(group)

    def renew_avatar_url(self, new_avatar_url: str):
        self.avatar_url = new_avatar_url

    def renew_commit_count(self, new_commit_count: int):
        self.commit_count = new_commit_count

    def change_username(self, new_username: str):
        self.username = new_username

    def approve(self):
        self.is_approved = True

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "avatar_url": self.avatar_url,
            "commit_count": self.commit_count,
            "is_approved": self.is_approved,
            "groups": self.groups,
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%dT%H:%M:%S"),
        }

    def __eq__(self, other):
        if not isinstance(other, GithubUser):
            return False
        return other.id == self.id

    def __hash__(self):
        return hash(self.id)