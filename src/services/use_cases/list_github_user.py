from typing import List
from src.entrypoints.schemas.github_user import GithubUserListRequestDto, GithubUserListResponseDto
from src.services.interfaces.repositories.github_user import AbstractGithubUserRepository
from src.services.interfaces.crawlers.github import AbstractCrawler


class GithubUserListUserCase:
    def __init__(self, repo: AbstractGithubUserRepository, crawler: AbstractCrawler):
        self.repo = repo
        self.crawler = crawler

    def execute(self, input_dto: GithubUserListResponseDto) -> List[GithubUserListRequestDto]:
        order_by_field = input_dto.order_by
        github_users = self.repo.list_github_user(
            filters=input_dto.filters,
            page=input_dto.page,
            per_page=input_dto.per_page,
            order_by_field=order_by_field,
        )  # List[GithubUser]

        return [GithubUserListResponseDto(**github_user.to_dict()) for github_user in github_users]
