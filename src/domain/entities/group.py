class Group:
    def __init__(self, id: int, name: str, category: str):
        self.id = id
        self.name = name
        self.category = category
        self.members = set()

    def change_category(self, new_caregory: str):
        self.category = new_caregory
