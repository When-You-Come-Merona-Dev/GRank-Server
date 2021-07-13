from src.github_user.services.unit_of_work import AbstractUnitOfWork
from src.github_user.entrypoints.schema import (
    GithubUserRetrieveResponseDto,
    GithubUserListRequestDto,
    GithubUserListResponseDto,
)


def retrieve_github_user(username: str, uow: AbstractUnitOfWork) -> GithubUserRetrieveResponseDto:
    with uow:
        github_user = uow.github_users.get_by_username(username)

        github_user_dict = github_user.to_dict()

    return GithubUserRetrieveResponseDto(**github_user_dict)


def list_github_user(
    input_dto: GithubUserListRequestDto, uow: AbstractUnitOfWork
) -> GithubUserListResponseDto:
    input_dto.filters["is_public"] = True

    with uow:
        github_users = uow.github_users.list(
            filters=input_dto.filters,
            page=input_dto.page,
            per_page=input_dto.per_page,
            order_by_field=input_dto.order_by,
        )
        github_users = [
            GithubUserListResponseDto(**github_user.to_dict()) for github_user in github_users
        ]

    return github_users