import os
import psycopg2
from urllib.parse import urlparse
from model.student import Student
from model.valuer import Valuer


class UsersDB:
    def __init__(self):
        url = urlparse(os.environ.get('DATABASE_URL'))
        self.db = "dbname={} user={} password={} host={} ".format(url.path[1:], url.username, url.password, url.hostname)

    def add_student(self, username, password, course, email):
        query = f'INSERT INTO STUDENT (username, password, course, email) VALUES (%s, %s, %s, %s);'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, (username, password, course, email))
                    conn.commit()
                    return True

                except psycopg2.IntegrityError:
                    return False

                except psycopg2.OperationalError:
                    return False

    def add_valuer(self, username, password):
        query = f'INSERT INTO VALUER (username, password) VALUES (%s, %s);'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, (username, password))
                    conn.commit()
                    return True

                except psycopg2.IntegrityError:
                    return False

                except psycopg2.OperationalError:
                    return False

    def get_student(self, email):
        query = f'SELECT * FROM STUDENT WHERE email = %s;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, (email,))
                    resp = cursor.fetchone()
                    if not resp:
                        return None

                    return self.create_student(resp)

                except psycopg2.ProgrammingError:
                    return None

    def get_valuer(self, username):
        query = f'SELECT * FROM VALUER WHERE username = %s;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, (username,))
                    resp = cursor.fetchone()
                    if not resp:
                        return None

                    return self.create_valuer(resp)

                except psycopg2.ProgrammingError:
                    return None

    def delete_student(self, email):
        query = f'DELETE FROM STUDENT WHERE email = %s;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, (email,))
                    conn.commit()
                    return True

                except psycopg2.OperationalError:
                    return False

                except psycopg2.IntegrityError:
                    return False

    def delete_valuer(self, username):
        query = f'DELETE FROM VALUER WHERE username = %s;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, (username,))
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

