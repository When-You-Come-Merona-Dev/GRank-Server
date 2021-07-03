from fastapi import HTTPException
from src.github_user.services.interfaces.repository import AbstractGithubUserRepository
from src.github_user.services.interfaces.crawler import AbstractCrawler
from src.github_user.entrypoints.schema import (
    GithubUserRenewOneRequestDto,
    GithubUserRenewOneResponseDto,
)


class GithubUserRenewOneUseCase:
    def __init__(self, repo: AbstractGithubUserRepository, crawler: AbstractCrawler):
        self.repo = repo
        self.crawler = crawler

    def execute(self, input_dto: GithubUserRenewOneRequestDto) -> GithubUserRenewOneResponseDto:
        github_user = self.repo.get_github_user_by_username(input_dto.username)
        if not github_user:
            raise HTTPException(status_code=404, detail="Can't find github user")

        new_avatar_url = self.crawler.get_avatar_url_from_username(input_dto.username)
        new_commit_count = self.crawler.get_commit_count_from_username(input_dto.username)

        github_user = self.repo.renew_avatar_url(github_user, new_avatar_url)
        renewed_github_user = self.repo.renew_commit_count(github_user, new_commit_count)

        output_dto = GithubUserRenewOneResponseDto(**renewed_github_user.to_dict())
        return output_dto
