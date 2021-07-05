from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from src.github_user.adapters.external_api import RequestExternalAPIClient
from src.infra.db.session import get_session
from src.user.adapters.repository import SQLAlchemyUserRepository
from src.user.entrypoints.schema import (
    SNSGithubCallbackRequestDto,
    SNSGithubCallbackResponseDto,
)
from src.user.services.use_cases.sns_github_login import SNSGithubLoginUseCase
from src.config import CONFIG

router = APIRouter()
security = HTTPBearer()


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
    repo = SQLAlchemyUserRepository(session)
    external_api = RequestExternalAPIClient()
    input_dto = SNSGithubCallbackRequestDto(code=code)

    use_case = SNSGithubLoginUseCase(repo=repo, external_api=external_api)

    output_dto = use_case.execute(input_dto)
    return output_dto
