class Admin:
    def __init__(self, username: str, password: str):
        self.id = None
        self.username = username
        self.password = password
        self.created_at = None
        self.updated_at = None


class AdminSecretCode:
    def __init__(self, code: str):
        self.code = code
        self.created_at = None
        self.updated_at = None
