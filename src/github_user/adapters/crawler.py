import json
from typing import Union
import requests
from bs4 import BeautifulSoup
from src.github_user.services.interfaces.crawler import AbstractCrawler


class RequestsGithubCrawler(AbstractCrawler):
    def get_commit_count_from_username(self, username) -> Union[int, None]:
        response = requests.get(f"https://github.com/users/{username}/contributions")
        if response.status_code == 404:
            return None

        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        first = soup.find("h2", "f4 text-normal mb-2")
        return int(first.get_text().split()[0].replace(",", ""))

    def get_avatar_url_from_username(self, username: str) -> str:
        response = requests.get(f"https://api.github.com/users/{username}")
        if response.status_code == 404:
            return None
        data = response.content.decode("utf8").replace("'", '"')
        github_user = json.loads(data)
        return github_user["avatar_url"]
