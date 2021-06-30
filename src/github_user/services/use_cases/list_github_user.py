from typing import List
from src.github_user.entrypoints.schema import GithubUserListRequestDto, GithubUserListResponseDto
from src.github_user.services.interfaces.repository import AbstractGithubUserRepository
from src.github_user.services.interfaces.crawler import AbstractCrawler


class GithubUserListUserCase:
    def __init__(self, repo: AbstractGithubUserRepository, crawler: AbstractCrawler):
        self.repo = repo
        self.crawler = crawler

    def execute(self, input_dto: GithubUserListResponseDto) -> List[GithubUserListRequestDto]:
        input_dto.filters["is_approved"] = True

        github_users = self.repo.list_github_user(
            filters=input_dto.filters,
            page=input_dto.page,
            per_page=input_dto.per_page,
            order_by_field=input_dto.order_by,
        )  # List[GithubUser]

        return [GithubUserListResponseDto(**github_user.to_dict()) for github_user in github_users]
