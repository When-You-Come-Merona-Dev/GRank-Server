from src.github_user.services.unit_of_work import AbstractUnitOfWork
from src.github_user.entrypoints.schema import GithubUserListRequestDto, GithubUserListResponseDto


def list_github_user(
    input_dto: GithubUserListRequestDto, uow: AbstractUnitOfWork
) -> GithubUserListResponseDto:
    input_dto.filters["is_approved"] = True
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