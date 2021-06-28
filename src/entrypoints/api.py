from src.domain.entities.github_user import GithubUser
from src.entrypoints import parsers
from typing import Optional, List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette import status
from src.config import CONFIG
from src.adapters.db.session import get_session
from src.adapters.crawlers.github import RequestsGithubCrawler
from src.adapters.repositories.github_user import GithubUserRepository
from src.entrypoints.parsers.query_parser import QueryParameterParser
from src.entrypoints.schemas.github_user import (
    GithubUserCreateRequestDto,
    GithubUserCreateResponseDto,
    GithubUserListResponseDto,
    GithubUserListRequestDto,
)
from src.services.use_cases.add_github_user import GithubUserAddUseCase
from src.services.use_cases.list_github_user import GithubUserListUserCase

router = APIRouter()


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
