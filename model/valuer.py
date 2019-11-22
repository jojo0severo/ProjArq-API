

class Valuer:
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def json(self):
        return {
            'name': self.name,
            'is_student': False
        }