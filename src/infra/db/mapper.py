from sqlalchemy.orm import clear_mappers
from src.admin.adapters.orm import start_mappers as admin_start_mappers
from src.github_user.adapters.orm import start_mappers as github_user_start_mappers


def start_mappers():
    clear_mappers()
    admin_start_mappers()
    github_user_start_mappers()