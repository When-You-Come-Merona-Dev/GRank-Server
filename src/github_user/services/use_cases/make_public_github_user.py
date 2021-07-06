from fastapi import HTTPException
from src.github_user.domain.entities.github_user import GithubUser
from src.github_user.services.interfaces.repository import AbstractGithubUserRepository
from src.github_user.entrypoints.schema import (
    GithubUserMakePublicRequestDto,
    GithubUserMakePublicResponseDto,
)


class GithubUserMakePublicUseCase:
    def __init__(self, repo: AbstractGithubUserRepository):
        self.repo = repo

    def execute(self, input_dto: GithubUserMakePublicRequestDto) -> GithubUserMakePublicResponseDto:
        github_user = self.repo.get_github_user_by_username(input_dto.username)
        if not github_user:
            raise HTTPException(status_code=404, detail="Can't find github user")
        public_github_user = self.repo.make_public_github_user(github_user)

        output_dto = GithubUserMakePublicResponseDto(**public_github_user.to_dict())
        return output_dto
