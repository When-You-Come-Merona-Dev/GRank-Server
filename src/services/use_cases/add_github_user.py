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

        exists_user = self.repo.get_github_user_by_username(input_dto.username)

        if exists_user:
            raise HTTPException(status_code=400, detail="already exists github username")

        commit_count = self.crawler.get_commit_count_from_username(input_dto.username)

        if commit_count == None:
            raise HTTPException(status_code=404, detail="not exists github user")

        github_user = GithubUser(username=input_dto.username)
        github_user.renew_commit_count(commit_count)

        self.repo.create_github_user(github_user)

        output_dto = GithubUserDTO(**github_user.to_dict())
        return output_dto
