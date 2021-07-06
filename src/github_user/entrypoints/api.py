from typing import Optional, List
from fastapi import security
from starlette import status
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Request, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.infra.db.session import get_session
from src.github_user.entrypoints.parsers.query_parser import QueryParameterParser
from src.github_user.entrypoints.schema import (
    GithubUserCreateRequestDto,
    GithubUserCreateResponseDto,
    GithubUserListResponseDto,
    GithubUserListRequestDto,
    GithubUserApproveResponseDto,
    GithubUserApproveRequestDto,
    GithubUserRenewAllRequestDto,
    GithubUserRenewAllResponseDto,
    GithubUserRenewOneRequestDto,
    GithubUserRenewOneResponseDto,
    SNSGithubCallbackRequestDto,
    SNSGithubCallbackResponseDto,
)
from src.github_user.adapters.external_api import RequestExternalAPIClient
from src.github_user.adapters.repository import GithubUserRepository
from src.github_user.services.use_cases.add_github_user import GithubUserAddUseCase
from src.github_user.services.use_cases.list_github_user import GithubUserListUserCase
from src.github_user.services.use_cases.approve_github_user import GithubUserApproveUseCase
from src.github_user.services.use_cases.renew_one_github_user import GithubUserRenewOneUseCase
from src.github_user.services.use_cases.renew_all_github_user import GithubUserRenewAllUseCase
from src.github_user.services.use_cases.sns_github_login import SNSGithubLoginUseCase
from src.utils.permissions import IsAdmin, check_permissions
from src.config import CONFIG

router = APIRouter()
security = HTTPBearer()
# TODO : api 구조화


@router.post(
    "/github-user",
    response_model=GithubUserCreateResponseDto,
    status_code=status.HTTP_201_CREATED,
)
def add_github_user(
    user: GithubUserCreateRequestDto, session: Session = Depends(get_session)
) -> GithubUserCreateResponseDto:
    crawler = RequestExternalAPIClient()
    repo = GithubUserRepository(session)

    use_case = GithubUserAddUseCase(repo=repo, crawler=crawler)

    output_dto = use_case.execute(user)
    return output_dto


@router.get(
    "/github-user", response_model=List[GithubUserListResponseDto], status_code=status.HTTP_200_OK
)
def list_github_user(
    request: Request,
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    order_by: Optional[str] = "commit_count",
    session: Session = Depends(get_session),
) -> List[GithubUserListResponseDto]:

    parser = QueryParameterParser(query=request.query_params)
    page, per_page = parser.parse_pagination_parameter()
    order_by = parser.parse_order_by_rule_parameter()

    crawler = None
    repo = GithubUserRepository(session)

    use_case = GithubUserListUserCase(repo=repo, crawler=crawler)

    request_dto = GithubUserListRequestDto(
        filters={}, page=page, per_page=per_page, order_by=order_by
    )

    response_dto = use_case.execute(request_dto)

    return response_dto


@router.patch(
    "/github-user/{username}/approve",
    response_model=GithubUserApproveResponseDto,
    status_code=status.HTTP_200_OK,
)
def approve_github_user(
    request: Request,
    username: str,
    session: Session = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> GithubUserApproveResponseDto:
    check_permissions(request=request, permissions=[IsAdmin])

    repo = GithubUserRepository(session)
    use_case = GithubUserApproveUseCase(repo=repo)
    input_dto = GithubUserApproveRequestDto(username=username)
    output_dto = use_case.execute(input_dto)
    return output_dto


@router.patch(
    "/github-user/{username}/renew",
    response_model=GithubUserRenewOneResponseDto,
    status_code=status.HTTP_200_OK,
)
def renew_one_github_user(
    username: str,
    session: Session = Depends(get_session),
) -> GithubUserRenewOneResponseDto:
    repo = GithubUserRepository(session)
    crawler = RequestExternalAPIClient()

    input_dto = GithubUserRenewOneRequestDto(username=username)

    use_case = GithubUserRenewOneUseCase(repo=repo, crawler=crawler)

    output_dto = use_case.execute(input_dto)
    return output_dto


@router.patch(
    "/github-user/renew-all",
    response_model=List[GithubUserRenewAllResponseDto],
    status_code=status.HTTP_200_OK,
)
def renew_all_github_user(
    request: Request,
    session: Session = Depends(get_session),
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> List[GithubUserRenewAllResponseDto]:
    check_permissions(request=request, permissions=[IsAdmin])

    repo = GithubUserRepository(session)
    crawler = RequestExternalAPIClient()

    input_dto = GithubUserRenewAllRequestDto()

    use_case = GithubUserRenewAllUseCase(repo=repo, crawler=crawler)

    output_dto = use_case.execute(input_dto)
    return output_dto


@router.get("/sns/github")
def get_github_login_url():
    url = "https://github.com/login/oauth/authorize?client_id={0}&redirect_uri={1}".format(
        CONFIG.GITHUB_API_CLIENT_ID, CONFIG.GITHUB_OAUTH_REDIRECT_URI
    )

    return {"login_url": url}


@router.get("/sns/github/callback")
def github_callback(
    code: str,
    session: Session = Depends(get_session),
) -> SNSGithubCallbackResponseDto:
    repo = GithubUserRepository(session)
    external_api = RequestExternalAPIClient()
    input_dto = SNSGithubCallbackRequestDto(code=code)

    use_case = SNSGithubLoginUseCase(repo=repo, external_api=external_api)

    output_dto = use_case.execute(input_dto)
    return output_dto
