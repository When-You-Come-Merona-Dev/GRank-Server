class User:
    def __init__(self, email: str, sns_service_id: str):
        self.id = None
        self.email = email
        self.sns_service_id = sns_service_id
