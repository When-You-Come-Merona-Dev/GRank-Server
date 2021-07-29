from typing import Optional
from src.github_user.services.unit_of_work import AbstractUnitOfWork
from src.github_user.adapters.external_api import (
    get_github_avatar_url_by_username,
    get_github_commit_count_by_username,
    get_github_oauth_token_by_code,
    get_github_user_by_oauth_token,
)
from src.github_user.entrypoints.schema import (
    GithubUserApproveRequestDto,
    GithubUserApproveResponseDto,
    GithubUserPartialUpdateResponseDto,
    GithubUserRenewAllRequestDto,
    GithubUserRenewAllResponseDto,
    GithubUserRenewOneRequestDto,
    GithubUserRenewOneResponseDto,
    GithubUserDeleteResponseDto,
    SNSGithubCallbackRequestDto,
    SNSGithubCallbackResponseDto,
)
from src.github_user.domain.entities.github_user import GithubUser
from src.utils.hasher import hash_password, check_password
from src.utils.token_handlers import jwt_encode_handler, jwt_payload_handler
from src.utils.exceptions import InvalidLoginCredentialsException, NotFoundGithubUserException


def approve_github_user(
    input_dto: GithubUserApproveRequestDto, uow: AbstractUnitOfWork
) -> GithubUserApproveResponseDto:
    with uow:
        github_user = uow.github_users.get_by_username(input_dto.username)
        if not github_user:
            raise NotFoundGithubUserException()
        github_user.approve()

        uow.commit()

    return GithubUserApproveResponseDto(detail="approve user successfully")


def partial_update_github_user(
    *, username: str, grade: Optional[int], is_public: Optional[bool], uow: AbstractUnitOfWork
) -> GithubUserPartialUpdateResponseDto:
    with uow:
        github_user = uow.github_users.get_by_username(username)
        if not github_user:
            raise NotFoundGithubUserException()

        if grade is not None:
            github_user.change_grade(grade)

        if is_public is not None:
            github_user.change_is_public(is_public)

        uow.commit()

        github_user_dict = github_user.to_dict()

    return GithubUserPartialUpdateResponseDto(**github_user_dict)


def renew_all_github_user(
    input_dto: GithubUserRenewAllRequestDto, uow: AbstractUnitOfWork
) -> GithubUserRenewAllResponseDto:
    filters = {"is_approved": True}

    with uow:
        github_users = uow.github_users.list(filters=filters)

        for github_user in github_users:
            new_avatar_url = get_github_avatar_url_by_username(github_user.username)
            new_commit_count = get_github_commit_count_by_username(github_user.username)

            github_user.renew_avatar_url(new_avatar_url)
            github_user.renew_commit_count(new_commit_count)

        uow.commit()

    return GithubUserRenewAllResponseDto(detail="renew all users info successfully")


def renew_one_github_user(
    input_dto: GithubUserRenewOneRequestDto, uow: AbstractUnitOfWork
) -> GithubUserRenewOneResponseDto:
    with uow:
        github_user = uow.github_users.get_by_username(username=input_dto.username)
        if not github_user:
            raise NotFoundGithubUserException()

        new_avatar_url = get_github_avatar_url_by_username(input_dto.username)
        new_commit_count = get_github_commit_count_by_username(input_dto.username)

        github_user.renew_avatar_url(new_avatar_url)
        github_user.renew_commit_count(new_commit_count)

        uow.commit()

    return GithubUserRenewOneResponseDto(detail="renew user info successfully")


def delete_github_user(username: str, uow: AbstractUnitOfWork) -> GithubUserDeleteResponseDto:
    with uow:
        github_user = uow.github_users.get_by_username(username)
        if not github_user:
            raise NotFoundGithubUserException()

        uow.github_users.delete(github_user)
        uow.commit()

    return GithubUserDeleteResponseDto(detail="deleted successfully")


def github_callback(
    input_dto: SNSGithubCallbackRequestDto, uow: AbstractUnitOfWork
) -> SNSGithubCallbackResponseDto:
    with uow:
        oauth_token = get_github_oauth_token_by_code(code=input_dto.code)
        user_info = get_github_user_by_oauth_token(oauth_token)

        github_id = user_info["id"]
        exists_user = uow.github_users.get_by_github_id(github_id=github_id)

        if exists_user:
            if check_password(user_info["node_id"], exists_user.password):
                user_instance = exists_user
            else:
                raise InvalidLoginCredentialsException()
        else:
            hashed_password = hash_password(user_info["node_id"])
            user_instance = GithubUser(
                github_id=github_id,
                password=hashed_password,
                username=user_info["login"],
                avatar_url=user_info["avatar_url"],
            )
            uow.github_users.add(github_user=user_instance)

        payload = jwt_payload_handler(user_instance)
        token = jwt_encode_handler(payload)

        uow.commit()

    return SNSGithubCallbackResponseDto(token=token)
