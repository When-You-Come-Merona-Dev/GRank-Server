class BaseException(Exception):
    status_code = 400

    def __init__(self):
        super().__init__()


class PermissionDeniedException(BaseException):
    status_code = 403

    def __init__(self):
        super().__init__()
        self.detail = f"You do not have permission to make this request."
