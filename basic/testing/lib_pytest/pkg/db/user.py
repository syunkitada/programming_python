class UserDb:
    def __init__(self):
        self.database = {}

    def insert(self, name, age):
        self.database[name] = {
            "name": name,
            "age": age,
        }

    def get(self, name):
        return self.database.get(name)
