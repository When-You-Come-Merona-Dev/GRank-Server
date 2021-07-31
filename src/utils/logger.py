import json
import logging
from datetime import timedelta, datetime
from time import time
from starlette.requests import Request
from fastapi.logger import logger

logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
# TODO : Custom logger handler 붙이기 (slack 메세지 전송 또는 파일 입력)


async def make_log(request: Request, response=None, error=None):
    time_format = "%Y-%m-%dT%H:%M:%S"
    t = time() - request.state.start
    status_code = response.status_code if response else error.status_code
    error_log_dict = None
    user = request.user

    if error:
        if hasattr(request.state, "inspect"):
            frame = request.state.inspect
            error_file = frame.f_code.co_filename
            error_func = frame.f_code.co_name
            error_line = frame.f_lineno
        else:
            error_func = error_file = error_line = "UNKNOWN"

        error_log_dict = dict(
            error_func=error_func,
            location="{} line in {}".format(str(error_line), error_file),
            raised=str(error.__class__.__name__),
            detail=str(error),
        )

    user_log = dict(
        client=request.state.ip,
        user=user.username if user and user.username else None,
        email=user.email if hasattr(user, "email") else None,
    )

    log_dict = dict(
        url=request.url.hostname + request.url.path,
        method=str(request.method),
        status_code=status_code,
        client=user_log,
        processed_time=str(round(t * 1000, 5)) + "ms",
        datetime_utc=datetime.utcnow().strftime(time_format),
        datetime_kst=(datetime.utcnow() + timedelta(hours=9)).strftime(time_format),
    )

    if error:
        logger.error(json.dumps(error_log_dict))
    else:
        logger.info(json.dumps(log_dict))