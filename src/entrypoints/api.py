from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status
from src.adapters.db.session import get_session
from src.adapters.crawlers.github import RequestsGithubCrawler
from src.adapters.repositories.github_user import GithubUserRepository
from src.services.dto.input import AddGithubUserDTO
from src.services.dto.output import GithubUserDTO
from src.services.use_cases.add_github_user import GithubUserAddUseCase

router = APIRouter()


@router.post("/github_user", response_model=GithubUserDTO, status_code=status.HTTP_201_CREATED)
def add_github_user(
    user: AddGithubUserDTO, session: Session = Depends(get_session)
) -> GithubUserDTO:
    crawler = RequestsGithubCrawler()
    repo = GithubUserRepository(session)

    use_case = GithubUserAddUseCase(repo=repo, crawler=crawler)

    output_dto = use_case.execute(user)
    return output_dto
