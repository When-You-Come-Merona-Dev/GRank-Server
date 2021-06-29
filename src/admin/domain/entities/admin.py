class Admin:
    def __init__(self, username: str, password: str):
        self.id = None
        self.username = username
        self.password = password
        self.created_at = None
        self.updated_at = None

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%dT%H:%M:%S"),
        }


class AdminCertificationCode:
    def __init__(self, code: str):
        self.code = code
        self.created_at = None
        self.updated_at = None

    def to_dict(self):
        return {
            "code": self.code,
            "created_at": self.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y-%m-%dT%H:%M:%S"),
        }