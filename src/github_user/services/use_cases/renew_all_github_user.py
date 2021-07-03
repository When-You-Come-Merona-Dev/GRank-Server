from typing import List
from fastapi import HTTPException
from src.github_user.services.interfaces.repository import AbstractGithubUserRepository
from src.github_user.services.interfaces.crawler import AbstractCrawler
from src.github_user.entrypoints.schema import (
    GithubUserRenewAllRequestDto,
    GithubUserRenewAllResponseDto,
)


class GithubUserRenewAllUseCase:
    def __init__(self, repo: AbstractGithubUserRepository, crawler: AbstractCrawler):
        self.repo = repo
        self.crawler = crawler

    def execute(
        self, input_dto: GithubUserRenewAllRequestDto
    ) -> List[GithubUserRenewAllResponseDto]:
        filters = {"is_approved": True}
        github_users = self.repo.list_github_user(filters=filters)

        renewed_github_users = []
        for github_user in github_users:
            new_avatar_url = self.crawler.get_avatar_url_from_username(github_user.username)
            new_commit_count = self.crawler.get_commit_count_from_username(github_user.username)
            github_user = self.repo.renew_avatar_url(github_user, new_avatar_url)
            renewed_github_user = self.repo.renew_commit_count(github_user, new_commit_count)
            renewed_github_users.append(
                GithubUserRenewAllResponseDto(**renewed_github_user.to_dict())
            )

        return renewed_github_users
