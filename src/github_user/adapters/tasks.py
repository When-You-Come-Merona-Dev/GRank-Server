from celery import Celery, Task
from src.infra.db.mapper import start_mappers
from src.github_user.adapters.external_api import (
    get_github_avatar_url_by_username,
    get_github_commit_count_by_username,
)
from src.github_user.services.unit_of_work import SQLAlchemyUnitOfWork

app = Celery("tasks", backend="redis://redis:6379", broker="amqp://guest:guest@rabbitmq:5672//")


class SQLAlchemyTask(Task):
    abstract = True

    def __call__(self, *args, **kwargs):
        start_mappers()
        return super().__call__(*args, **kwargs)


@app.task(base=SQLAlchemyTask)
def renew_github_users():
    uow = SQLAlchemyUnitOfWork()

    filters = {"is_approved": True}

    with uow:
        github_users = uow.github_users.list(filters=filters)

        for github_user in github_users:
            new_avatar_url = get_github_avatar_url_by_username(github_user.username)
            new_commit_count = get_github_commit_count_by_username(github_user.username)
            github_user.renew_avatar_url(new_avatar_url)
            github_user.renew_commit_count(new_commit_count)

        uow.commit()

    return "OK"
