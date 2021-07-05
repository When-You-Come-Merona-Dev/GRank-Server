from src.github_user.domain.entities.github_user import GithubUser


class SocialAuthentication:
    def __init__(self, github_user: GithubUser, sns_service_id):
        self.id = None
        self.github_user_id = github_user.id
        self.sns_service_id = sns_service_id
