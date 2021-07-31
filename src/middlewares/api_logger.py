import time
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response
from fastapi import Request
from src.utils.logger import make_log
from src.utils.exceptions import APIException


class APILoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request.state.start = time.time()

        ip = (
            request.headers["x-forwarded-for"]
            if "x-forwarded-for" in request.headers.keys()
            else request.client.host
        )
        request.state.ip = ip.split(",")[0] if "," in ip else ip
        try:
            response = await call_next(request)
            await make_log(request=request, response=response)
        except Exception as e:
            error = await exception_handler(e)
            error_dict = dict(status=error.status_code, detail=error.detail, code=error.code)
            response = JSONResponse(status_code=error.status_code, content=error_dict)
            await make_log(request=request, error=error)

        return response


async def exception_handler(error: Exception):
    if not isinstance(error, APIException):
        error = APIException(ex=error, detail=str(error))

    return error