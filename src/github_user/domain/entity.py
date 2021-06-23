class Group:
    def __init__(self, id: int, name: str, category: str):
        self.id = id
        self.name = name
        self.category = category

    def change_category(self, new_caregory: str):
        self.category = new_caregory


class GithubUser:
    def __init__(self, id: int, username: str, commit_count: int):
        self.id = id
        self.username = username
        self.commit_count = commit_count
        self.is_approved = False
        self._groups = set()

    def join_group(self, group: Group):
        self._groups.add(group)

    def leave_group(self, group: Group):
        if group in self._groups:
            self._groups.remove(group)

    def renew_commit_count(self, new_commit_count: int):
        self.commit_count = new_commit_count

    def change_username(self, new_username: str):
        self.username = new_username

    def change_major_club(self, new_major_club: str):
        self.majot_club = new_major_club

    def approve(self):
        self.is_approved = True

    def __eq__(self, other):
        if not isinstance(other, GithubUser):
            return False
        return other.id == self.id

    def __hash__(self):
        return hash(self.id)