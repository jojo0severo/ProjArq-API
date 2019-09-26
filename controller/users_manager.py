from model.valuer import Valuer
from model.student import Student
from model.users_database import UsersDB


class UsersManager:
    def __init__(self):
        self.students = {}
        self.valuers = {}
        self.users_database = UsersDB()

    def add_user(self, username, password, is_student, course, email):
        if is_student:
            if username not in self.students.keys():
                if self.users_database.add_student(username, password, course, email):
                    self.students[email] = Student(username, password, course, email)
                    return True

            return False

        else:
            if username not in self.valuers.keys():
                if self.users_database.add_valuer(username, password):
                    self.valuers[username] = Valuer(username, password)
                    return True

            return False

    def get_user(self, key, is_student):
        if is_student:
            if key not in self.students.keys():
                return self.users_database.get_student(key)

            return self.students[key]

        else:
            if key not in self.valuers.keys():
                return self.users_database.get_valuer(key)

            return self.valuers[key]

    def remove_user(self, key, is_student):
        if is_student:
            if key in self.students.keys():
                del self.students[key]

            return self.users_database.delete_student(key)

        else:
            if key in self.valuers.keys():
                del self.valuers[key]

            return self.users_database.delete_valuer(key)

    def check_user(self, key, password, is_student):
        if is_student:
            if key not in self.students.keys():
                student = self.users_database.get_student(key)
                if student is not None:
                    self.students[key] = student
                    return student.password == password

                return False

            return self.students[key].password == password

        else:
            if key not in self.valuers.keys():
                valuer = self.users_database.get_valuer(key)
                if valuer is not None:
                    self.valuers[key] = valuer
                    return valuer.password == password

                return False

            return self.valuers[key].password == password
