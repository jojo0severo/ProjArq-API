class Student:
    def __init__(self, username, password, course, email):
        self.username = username
        self.password = password
        self.course = course
        self.email = email

    def json(self):
        return {
            'name': self.username.split('@')[0].replace('_', ' '),
            'email': self.email,
            'course': self.course,
            'is_student': True
        }
