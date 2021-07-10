from typing import List, Optional
from fastapi import HTTPException
from src.github_user.services.unit_of_work import AbstractUnitOfWork
from src.github_user.adapters import external_api
from src.github_user.entrypoints.schema import (
    GithubUserApproveRequestDto,
    GithubUserApproveResponseDto,
    GithubUserPartialUpdateRequestDto,
    GithubUserPartialUpdateResponseDto,
    GithubUserRenewAllRequestDto,
    GithubUserRenewAllResponseDto,
    GithubUserRenewOneRequestDto,
    GithubUserRenewOneResponseDto,
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
        approved_github_user = uow.github_users.approve(github_user)

        uow.commit()

        approved_github_user_dict = approved_github_user.to_dict()

    return GithubUserApproveResponseDto(**approved_github_user_dict)


def partial_update_github_user(
    *, username: str, grade: Optional[int], is_public: Optional[bool], uow: AbstractUnitOfWork
) -> GithubUserPartialUpdateResponseDto:
    with uow:
        github_user = uow.github_users.get_by_username(username)
        if not github_user:
            raise NotFoundGithubUserException()

        if grade is not None:
            github_user.grade = grade

        if is_public is not None:
            github_user.is_public = is_public

        uow.commit()

        github_user_dict = github_user.to_dict()

    return GithubUserPartialUpdateResponseDto(**github_user_dict)


def renew_all_github_user(
    input_dto: GithubUserRenewAllRequestDto, uow: AbstractUnitOfWork
) -> List[GithubUserRenewAllResponseDto]:
    filters = {"is_approved": True}

    with uow:
        github_users = uow.github_users.list(filters=filters)
        renewed_github_users = []
        for github_user in github_users:
            new_avatar_url = external_api.get_avatar_url_from_username(github_user.username)
            new_commit_count = external_api.get_commit_count_from_username(github_user.username)

            github_user = uow.github_users.renew_avatar_url(github_user, new_avatar_url)
            renewed_github_user = uow.github_users.renew_commit_count(github_user, new_commit_count)
            renewed_github_users.append(
                GithubUserRenewAllResponseDto(**renewed_github_user.to_dict())
            )

        uow.commit()

    return renewed_github_users


def renew_one_github_user(
    input_dto: GithubUserRenewOneRequestDto, uow: AbstractUnitOfWork
) -> GithubUserRenewOneResponseDto:
    with uow:
        github_user = uow.github_users.get_by_username(username=input_dto.username)
        if not github_user:
            raise NotFoundGithubUserException()

        new_avatar_url = external_api.get_avatar_url_from_username(input_dto.username)
        new_commit_count = external_api.get_commit_count_from_username(input_dto.username)

        github_user = uow.github_users.renew_avatar_url(github_user, new_avatar_url)
        renewed_github_user = uow.github_users.renew_commit_count(github_user, new_commit_count)

        uow.commit()

        renewed_github_user_dict = renewed_github_user.to_dict()

    return GithubUserRenewOneResponseDto(**renewed_github_user_dict)


def github_callback(
    input_dto: SNSGithubCallbackRequestDto, uow: AbstractUnitOfWork
) -> SNSGithubCallbackResponseDto:
    with uow:
        oauth_token = external_api.get_github_oauth_token(code=input_dto.code)
        user_info = external_api.get_github_user_info(oauth_token)

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
