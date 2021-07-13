from typing import Optional, List
from fastapi import security
from starlette import status
from fastapi import APIRouter, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.github_user.entrypoints.parsers.query_parser import QueryParameterParser
from src.github_user.entrypoints.schema import (
    GithubUserDeleteResponseDto,
    GithubUserListResponseDto,
    GithubUserRetrieveResponseDto,
    GithubUserRetrieveRequestDto,
    GithubUserListRequestDto,
    GithubUserApproveResponseDto,
    GithubUserApproveRequestDto,
    GithubUserPartialUpdateRequestDto,
    GithubUserPartialUpdateResponseDto,
    GithubUserRenewAllRequestDto,
    GithubUserRenewAllResponseDto,
    GithubUserRenewOneRequestDto,
    GithubUserRenewOneResponseDto,
    SNSGithubCallbackRequestDto,
    SNSGithubCallbackResponseDto,
)
from src.github_user.services.unit_of_work import SQLAlchemyUnitOfWork
from src.github_user.services import handlers, readers
from src.utils.permissions import IsAdmin, IsAuthenticated, IsOwnerOrAdmin, check_permissions
from src.utils.exceptions import NotFoundGithubUserException
from src.config import CONFIG

router = APIRouter()
security = HTTPBearer()


@router.get(
    "/github-users",
    response_model=List[GithubUserListResponseDto],
    status_code=status.HTTP_200_OK,
    tags=["github-users"],
)
def list_github_user(
    request: Request,
    is_approved: Optional[bool] = True,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    order_by: Optional[str] = "commit_count",
) -> List[GithubUserListResponseDto]:

    parser = QueryParameterParser(query=request.query_params)
    page, per_page = parser.parse_pagination_parameter()
    order_by = parser.parse_order_by_rule_parameter()

    input_dto = GithubUserListRequestDto(
        filters={"is_approved": is_approved}, page=page, per_page=per_page, order_by=order_by
    )

    return readers.list_github_user(input_dto=input_dto, uow=SQLAlchemyUnitOfWork())


@router.get(
    "/github-users/me",
    response_model=GithubUserRetrieveResponseDto,
    status_code=status.HTTP_200_OK,
    tags=["github-users"],
)
def retrieve_token_owner_github_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> GithubUserRetrieveResponseDto:
    check_permissions(request=request, permissions=[IsAuthenticated])
    username = getattr(request.user, "username", None)
    if not username:
        raise NotFoundGithubUserException()
    return readers.retrieve_github_user(username=username, uow=SQLAlchemyUnitOfWork())


@router.get(
    "/github-users/{username}",
    response_model=GithubUserRetrieveResponseDto,
    status_code=status.HTTP_200_OK,
    tags=["github-users"],
)
def retrieve_github_user(
    username: str,
) -> GithubUserRetrieveResponseDto:
    return readers.retrieve_github_user(username=username, uow=SQLAlchemyUnitOfWork())


@router.delete(
    "/github-users/{username}",
    response_model=GithubUserDeleteResponseDto,
    status_code=status.HTTP_200_OK,
    tags=["github-users"],
)
def delete_github_user(
    request: Request,
    username: str,
) -> GithubUserDeleteResponseDto:
    check_permissions(request=request, permissions=[IsOwnerOrAdmin])
    return handlers.delete_github_user(username=username, uow=SQLAlchemyUnitOfWork())


@router.patch(
    "/github-users/{username}",
    response_model=GithubUserPartialUpdateResponseDto,
    status_code=status.HTTP_200_OK,
    tags=["github-users"],
)
def partial_update_github_user(
    request: Request,
    username: str,
    input_dto: GithubUserPartialUpdateRequestDto,
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> GithubUserPartialUpdateResponseDto:
    check_permissions(request=request, permissions=[IsOwnerOrAdmin])

    return handlers.partial_update_github_user(
        username=username,
        grade=input_dto.grade,
        is_public=input_dto.is_public,
        uow=SQLAlchemyUnitOfWork(),
    )


@router.patch(
    "/github-users/{username}/approve",
    response_model=GithubUserApproveResponseDto,
    status_code=status.HTTP_200_OK,
    tags=["github-users"],
)
def approve_github_user(
    request: Request,
    username: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> GithubUserApproveResponseDto:
    check_permissions(request=request, permissions=[IsAdmin])

    input_dto = GithubUserApproveRequestDto(username=username)

    return handlers.approve_github_user(input_dto=input_dto, uow=SQLAlchemyUnitOfWork())


@router.patch(
    "/github-users/{username}/renew",
    response_model=GithubUserRenewOneResponseDto,
    status_code=status.HTTP_200_OK,
    tags=["github-users"],
)
def renew_one_github_user(
    request: Request,
    username: str,
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> GithubUserRenewOneResponseDto:
    check_permissions(request=request, permissions=[IsOwnerOrAdmin])

    input_dto = GithubUserRenewOneRequestDto(username=username)

    return handlers.renew_one_github_user(input_dto=input_dto, uow=SQLAlchemyUnitOfWork())


@router.patch(
    "/github-users/renew-all",
    response_model=List[GithubUserRenewAllResponseDto],
    status_code=status.HTTP_200_OK,
    tags=["github-users"],
)
def renew_all_github_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> List[GithubUserRenewAllResponseDto]:
    check_permissions(request=request, permissions=[IsAdmin])

    input_dto = GithubUserRenewAllRequestDto()

    return handlers.renew_all_github_user(input_dto=input_dto, uow=SQLAlchemyUnitOfWork())


@router.get("/sns/github", tags=["sns"])
def get_github_login_url():
    url = "https://github.com/login/oauth/authorize?client_id={0}&redirect_uri={1}".format(
        CONFIG.GITHUB_API_CLIENT_ID, CONFIG.GITHUB_OAUTH_REDIRECT_URI
    )

    return {"login_url": url}


@router.get("/sns/github/callback", tags=["sns"])
def github_callback(
    code: str,
) -> SNSGithubCallbackResponseDto:
    input_dto = SNSGithubCallbackRequestDto(code=code)

    return handlers.github_callback(input_dto=input_dto, uow=SQLAlchemyUnitOfWork())
