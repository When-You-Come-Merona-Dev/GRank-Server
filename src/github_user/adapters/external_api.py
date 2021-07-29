import json
from typing import Union
import requests
from bs4 import BeautifulSoup
from starlette import status
from fastapi import HTTPException
from src.config import CONFIG


def get_github_commit_count_by_username(username) -> Union[int, None]:
    response = requests.get(f"https://github.com/users/{username}/contributions")
    if response.status_code == status.HTTP_404_NOT_FOUND:
        return None

    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    first = soup.find("h2", "f4 text-normal mb-2")
    return int(first.get_text().split()[0].replace(",", ""))


def get_github_avatar_url_by_username(username: str) -> str:
    response = requests.get(
        f"https://api.github.com/users/{username}",
        headers={"Authorization": f"Bearer {CONFIG.GITHUB_API_TOKEN}"},
    )
    if response.status_code == status.HTTP_404_NOT_FOUND:
        return None
    if response.status_code == status.HTTP_403_FORBIDDEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="잠시 후에 시도해주세요, Github API가 1시간당 받을 수 있는 요청 갯수를 초과했습니다.",
        )
    data = response.content.decode("utf8")
    github_user = json.loads(data)
    return github_user["avatar_url"]


def get_github_oauth_token_by_code(code) -> str:
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "code": code,
            "client_id": CONFIG.GITHUB_API_CLIENT_ID,
            "client_secret": CONFIG.GITHUB_API_CLIENT_SECRET,
        },
        headers={"accept": "application/json"},
    )
    token_info = response.json()
    try:
        oauth_token = token_info["access_token"]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to retrieve oauth token"
        )
    return oauth_token


def get_github_user_by_oauth_token(oauth_token) -> str:
    response = requests.get(
        "https://api.github.com/user", headers={"Authorization": "token " + oauth_token}
    )
    if response.status_code not in (status.HTTP_200_OK,):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not access to resource with received oauth token",
        )

    return response.json()
