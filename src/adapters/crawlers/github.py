import requests
from bs4 import BeautifulSoup
from src.services.interfaces.crawlers.github import AbstractCrawler
from typing import Union


class RequestsGithubCrawler(AbstractCrawler):
    def get_commit_count_from_username(self, username) -> Union[int, None]:
        response = requests.get(f"https://github.com/users/{username}/contributions")
        if response.status_code == 404:
            return None

        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        first = soup.find("h2", "f4 text-normal mb-2")
        return int(first.get_text().split()[0].replace(",", ""))
