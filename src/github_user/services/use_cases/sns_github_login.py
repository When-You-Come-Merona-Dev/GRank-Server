from fastapi.exceptions import HTTPException
from src.github_user.services.interfaces.external_api import AbstractExternalAPIClient
from src.github_user.entrypoints.schema import (
    SNSGithubCallbackRequestDto,
    SNSGithubCallbackResponseDto,
)
from src.github_user.services.interfaces.repository import AbstractGithubUserRepository
from src.github_user.domain.entities.github_user import GithubUser
from src.utils.hasher import hash_password, check_password
from src.utils.token_handlers import jwt_encode_handler, jwt_payload_handler


class SNSGithubLoginUseCase:
    def __init__(self, repo: AbstractGithubUserRepository, external_api: AbstractExternalAPIClient):
        self.repo = repo
        self.external_api = external_api

    def execute(self, input_dto: SNSGithubCallbackRequestDto) -> SNSGithubCallbackResponseDto:
        oauth_token = self.external_api.get_github_oauth_token(code=input_dto.code)
        user_info = self.external_api.get_github_user_info(oauth_token)

        github_id = user_info["id"]
        exists_user = self.repo.get_user_by_github_id(github_id=github_id)

        if exists_user:
            if check_password(user_info["node_id"], exists_user.password):
                user_instance = exists_user
            else:
                raise HTTPException(status_code=400, detail="Can't login with recieved credentials")
        else:
            hashed_password = hash_password(user_info["node_id"])
            user_instance = GithubUser(
                github_id=github_id,
                password=hashed_password,
                username=user_info["login"],
                avatar_url=user_info["avatar_url"],
            )
            self.repo.create_github_user(github_user=user_instance)

        payload = jwt_payload_handler(user_instance)
        token = jwt_encode_handler(payload)

        output_dto = SNSGithubCallbackResponseDto(token=token)

        return output_dto