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
)
from src.github_user.adapters.crawler import RequestsGithubCrawler
from src.github_user.adapters.repository import GithubUserRepository
from src.github_user.services.use_cases.add_github_user import GithubUserAddUseCase
from src.github_user.services.use_cases.list_github_user import GithubUserListUserCase
from src.github_user.services.use_cases.approve_github_user import GithubUserApproveUseCase
from src.github_user.services.use_cases.renew_one_github_user import GithubUserRenewOneUseCase
from src.github_user.services.use_cases.renew_all_github_user import GithubUserRenewAllUseCase
from src.utils.permissions import IsAuthenticated, check_permissions

router = APIRouter()
security = HTTPBearer()


@router.post(
    "/github-user",
    response_model=GithubUserCreateResponseDto,
    status_code=status.HTTP_201_CREATED,
)
def add_github_user(
    user: GithubUserCreateRequestDto, session: Session = Depends(get_session)
) -> GithubUserCreateResponseDto:
    crawler = RequestsGithubCrawler()
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
    check_permissions(request=request, permissions=[IsAuthenticated])

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
    crawler = RequestsGithubCrawler()

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
    check_permissions(request=request, permissions=[IsAuthenticated])

    repo = GithubUserRepository(session)
    crawler = RequestsGithubCrawler()

    input_dto = GithubUserRenewAllRequestDto()

    use_case = GithubUserRenewAllUseCase(repo=repo, crawler=crawler)

    output_dto = use_case.execute(input_dto)
    return output_dto