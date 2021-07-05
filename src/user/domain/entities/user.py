class User:
    def __init__(self, github_id: str, password: str):
        self.id = None
        self.github_id = github_id
        self.password = password
        self.created_at = None
        self.updated_at = None

    def to_dict(self):
        return {
            "id": self.id,
            "github_id": self.github_id,
            "password": self.password,
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%dT%H:%M:%S"),
        }