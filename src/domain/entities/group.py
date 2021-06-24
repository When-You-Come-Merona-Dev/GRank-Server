class Group:
    def __init__(self, name: str, category: str):
        self.id = None
        self.name = name
        self.category = category
        self.members = set()

    def change_category(self, new_caregory: str):
        self.category = new_caregory
