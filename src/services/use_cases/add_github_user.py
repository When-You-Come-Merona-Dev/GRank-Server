from fastapi import HTTPException
from src.domain.entities.github_user import GithubUser
from src.services.dto.input import AddGithubUserDTO
from src.services.dto.output import GithubUserDTO
from src.services.interfaces.repositories.github_user import AbstractGithubUserRepository
from src.services.interfaces.crawlers.github import AbstractCrawler


class GithubUserAddUseCase:
    def __init__(self, repo: AbstractGithubUserRepository, crawler: AbstractCrawler):
        self.repo = repo
        self.crawler = crawler

    def execute(self, input_dto: AddGithubUserDTO) -> GithubUserDTO:
        commit_count = self.crawler.get_commit_count_from_username(input_dto.username)

        if commit_count == None:
            raise HTTPException(status_code=404, detail="not exists github user")

        github_user = GithubUser(username=input_dto.username)
        github_user.renew_commit_count(commit_count)

        self.repo.create_github_user(github_user)

        output_dto = GithubUserDTO(
            id=github_user.id,
            username=github_user.username,
            commit_count=github_user.commit_count,
            is_approved=github_user.is_approved,
            groups=github_user.groups,
        )
        return output_dto
