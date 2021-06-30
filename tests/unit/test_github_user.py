from src.github_user.domain.entities.group import Group
from src.github_user.domain.entities.github_user import GithubUser


def make_github_user_and_group(github_user_name: str = "test_user", group_name: str = "test_group"):
    github_user = GithubUser(github_user_name)
    group = Group(name=group_name, category="major")

    return github_user, group


def test_join_group():
    github_user, group = make_github_user_and_group()

    github_user.join_group(group)

    assert len(github_user.groups) == 1
    assert github_user.groups.pop() == group


def test_join_group_is_idempotent():
    github_user, group = make_github_user_and_group()

    github_user.join_group(group)
    github_user.join_group(group)

    assert len(github_user.groups) == 1
    assert github_user.groups.pop() == group


def test_leave_group_if_joined():
    github_user, group = make_github_user_and_group()

    github_user.join_group(group)
    github_user.leave_group(group)

    assert group not in github_user.groups


def test_renew_commit_count():
    github_user, _ = make_github_user_and_group()

    github_user.renew_commit_count(10)

    assert github_user.commit_count == 10


def test_change_username():
    github_user, _ = make_github_user_and_group(github_user_name="first_name")
    new_username = "new_username"
    github_user.change_username(new_username)

    assert github_user.username == new_username


def test_approve():
    github_user, _ = make_github_user_and_group()
    github_user.approve()
    assert github_user.is_approved == True