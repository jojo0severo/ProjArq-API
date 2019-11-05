import os
import psycopg2
from urllib.parse import urlparse
from model.certificate import Certificate


class CertificatesDB:
    def __init__(self):
        url = urlparse(os.environ.get('DATABASE_URL'))
        self.db = "dbname={} user={} password={} host={} ".format(url.path[1:], url.username, url.password, url.hostname)

    def get_certificate(self, email):
        query = f'SELECT * FROM CERTIFICATE WHERE username = %s;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, (email,))
                    resp = cursor.fetchone()
                    if not resp:
                        return None

                    return self.create_certificate(resp)

                except psycopg2.ProgrammingError:
                    return None

    def get_certificates(self):
        query = f'SELECT * FROM CERTIFICATE;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query)
                    certificates = cursor.fetchall()
                    certificates_objects = []
                    for certificate in certificates:
                        certificates_objects.append(self.create_certificate(certificate))

                    return certificates_objects

                except psycopg2.ProgrammingError:
                    return []

    def generate_certificate(self, username, team_name, date):
        query = f'INSERT INTO CERTIFICATE (username, team_name, generation_date) VALUES (%s, %s, %s);'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, (username, team_name, date))
                    conn.commit()
                    return True

                except psycopg2.IntegrityError:
                    return False

    def create_certificate(self, query_result):
        if not query_result:
            return None

        return Certificate(*query_result[1:])
