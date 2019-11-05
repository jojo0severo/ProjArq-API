import os
import psycopg2
from urllib.parse import urlparse
from model.student import Student
from model.valuer import Valuer


class UsersDB:
    def __init__(self):
        url = urlparse(os.environ.get('DATABASE_URL'))
        url = urlparse(
            'postgres://jiyhwfshwvzgom:10aa9f8bce9d36f1271749b82fce10459907a52c80f33f388f995ec36e2bfb4a@ec2-174-129-253-104.compute-1.amazonaws.com:5432/db3r8ta6ni6o1n')
        self.db = "dbname={} user={} password={} host={} ".format(url.path[1:], url.username, url.password, url.hostname)

    def add_student(self, username, password, course, email):
        query = f'INSERT INTO STUDENT VALUES ("{username}", "{password}", "{course}", "{email}");'

        with psycopg2.connect(self.db) as conn:
            try:
                conn.cursor().execute(query)
                return True

            except psycopg2.IntegrityError:
                return False

            except psycopg2.OperationalError:
                return False

    def add_valuer(self, username, password):
        query = f'INSERT INTO VALUER VALUES ("{username}", "{password}");'

        with psycopg2.connect(self.db) as conn:
            try:
                conn.cursor().execute(query)
                return True

            except psycopg2.IntegrityError:
                return False

            except psycopg2.OperationalError:
                return False

    def get_student(self, email):
        query = f'SELECT * FROM STUDENT WHERE email = "{email}";'

        with psycopg2.connect(self.db) as conn:
            conn.cursor().execute(query)
            resp = conn.cursor().fetchone()
            if not resp:
                return None

            return self.create_student(resp)

    def get_valuer(self, username):
        query = f'SELECT * FROM VALUER WHERE username = "{username}";'

        with psycopg2.connect(self.db) as conn:
            conn.cursor().execute(query)
            resp = conn.cursor().fetchone()
            if not resp:
                return None

            return self.create_valuer(resp)

    def delete_student(self, email):
        query = f'DELETE FROM STUDENT WHERE email = "{email}";'

        with psycopg2.connect(self.db) as conn:
            try:
                conn.cursor().execute(query)
                return True

            except psycopg2.OperationalError:
                return False

            except psycopg2.IntegrityError:
                return False

    def delete_valuer(self, username):
        query = f'DELETE FROM VALUER WHERE username = "{username}";'

        with psycopg2.connect(self.db) as conn:
            try:
                conn.cursor().execute(query)
                return True

            except psycopg2.OperationalError:
                return False

            except psycopg2.IntegrityError:
                return False

    def create_student(self, query_result):
        if not query_result:
            return None

        return Student(*query_result)

    def create_valuer(self, query_result):
        if not query_result:
            return None

        return Valuer(*query_result)

