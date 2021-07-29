import time
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from fastapi import Request
from src.utils.logger import make_log


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
            error = e
            await make_log(request=request, error=error)

        return response
