from fastapi import HTTPException
from src.github_user.services.interfaces.repository import AbstractGithubUserRepository
from src.github_user.services.interfaces.external_api import AbstractExternalAPIClient
from src.github_user.entrypoints.schema import (
    GithubUserRenewOneRequestDto,
    GithubUserRenewOneResponseDto,
)


class GithubUserRenewOneUseCase:
    def __init__(self, repo: AbstractGithubUserRepository, external_api: AbstractExternalAPIClient):
        self.repo = repo
        self.external_api = external_api

    def execute(self, input_dto: GithubUserRenewOneRequestDto) -> GithubUserRenewOneResponseDto:
        github_user = self.repo.get_github_user_by_username(input_dto.username)
        if not github_user:
            raise HTTPException(status_code=404, detail="Can't find github user")

        new_avatar_url = self.external_api.get_avatar_url_from_username(input_dto.username)
        new_commit_count = self.external_api.get_commit_count_from_username(input_dto.username)

        github_user = self.repo.renew_avatar_url(github_user, new_avatar_url)
        renewed_github_user = self.repo.renew_commit_count(github_user, new_commit_count)

        output_dto = GithubUserRenewOneResponseDto(**renewed_github_user.to_dict())
        return output_dto
