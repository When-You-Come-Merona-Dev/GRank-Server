from starlette import status


class APIException(Exception):
    status_code: int
    code: str
    msg: str
    detail: str

    def __init__(
        self,
        *,
        status_code: int = status.HTTP_503_SERVICE_UNAVAILABLE,
        code: str = "000000",  # 예외처리 종류 많아지면 code list 만들자
        detail: str = None,
        ex: Exception = None,
    ):
        self.status_code = status_code
        self.code = code
        self.detail = detail
        super().__init__(ex)


class PermissionDeniedException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="000000",
            detail=f"You do not have permission to make this request.",
            ex=ex,
        )


class NotFoundGithubUserException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="000000",
            detail=f"Can't find github user",
            ex=ex,
        )


class AlreadyExistAdminException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="000000",
            detail=f"already exists admin username",
            ex=ex,
        )


class InvalidAdminCertificationCodeException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="000000",
            detail=f"certification code is not available",
            ex=ex,
        )


class InvalidLoginCredentialsException(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="000000",
            detail=f"Can't login with recieved credentials",
            ex=ex,
        )
