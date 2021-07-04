import json
from typing import Union
import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException
from src.github_user.services.interfaces.crawler import AbstractCrawler
from src.config import CONFIG


class RequestsGithubCrawler(AbstractCrawler):
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {CONFIG.GITHUB_API_TOKEN}"}

    def get_commit_count_from_username(self, username) -> Union[int, None]:
        response = requests.get(f"https://github.com/users/{username}/contributions")
        if response.status_code == 404:
            return None

        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        first = soup.find("h2", "f4 text-normal mb-2")
        return int(first.get_text().split()[0].replace(",", ""))

    def get_avatar_url_from_username(self, username: str) -> str:
        response = requests.get(f"https://api.github.com/users/{username}", headers=self.headers)
        if response.status_code == 404:
            return None
        if response.status_code == 403:
            raise HTTPException(
                status_code=403, detail="잠시 후에 시도해주세요, Github API가 1시간당 받을 수 있는 요청 갯수를 초과했습니다."
            )
        data = response.content.decode("utf8").replace("'", '"')
        github_user = json.loads(data)
        return github_user["avatar_url"]
