import sqlite3
from model.student import Student
from model.valuer import Valuer


class UsersDB:

    def add_student(self, username, password, course, email):
        query = f'INSERT INTO STUDENT VALUES ("{username}", "{password}", "{course}", "{email}");'

        with sqlite3.connect('database/local.db') as conn:
            try:
                conn.cursor().execute(query)
                return True

            except sqlite3.IntegrityError:
                return False

            except sqlite3.OperationalError:
                return False

    def add_valuer(self, username, password):
        query = f'INSERT INTO VALUER VALUES ("{username}", "{password}");'

        with sqlite3.connect('database/local.db') as conn:
            try:
                conn.cursor().execute(query)
                return True

            except sqlite3.IntegrityError:
                return False

            except sqlite3.OperationalError:
                return False

    def get_student(self, email):
        query = f'SELECT * FROM STUDENT WHERE email = "{email}";'

        with sqlite3.connect('database/local.db') as conn:
            resp = conn.cursor().execute(query).fetchall()
            if not resp:
                return None

            return self.create_student(resp[0])

    def get_valuer(self, username):
        query = f'SELECT * FROM VALUER WHERE username = "{username}";'

        with sqlite3.connect('database/local.db') as conn:
            resp = conn.cursor().execute(query).fetchall()
            if not resp:
                return None

            return self.create_valuer(resp[0])

    def delete_student(self, email):
        query = f'DELETE FROM STUDENT WHERE email = "{email}";'

        with sqlite3.connect('database/local.db') as conn:
            try:
                conn.cursor().execute(query)
                return True

            except sqlite3.OperationalError:
                return False

            except sqlite3.IntegrityError:
                return False

    def delete_valuer(self, username):
        query = f'DELETE FROM VALUER WHERE username = "{username}";'

        with sqlite3.connect('database/local.db') as conn:
            try:
                conn.cursor().execute(query)
                return True

            except sqlite3.OperationalError:
                return False

            except sqlite3.IntegrityError:
                return False

    def create_student(self, query_result):
        if not query_result:
            return None

        return Student(*query_result)

    def create_valuer(self, query_result):
        if not query_result:
            return None

        return Valuer(*query_result)

