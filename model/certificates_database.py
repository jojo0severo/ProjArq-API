import os
import psycopg2
from urllib.parse import urlparse
from model.certificate import Certificate


class CertificatesDB:
    def __init__(self):
        url = urlparse(os.environ.get('DATABASE_URL'))
        url = urlparse('postgres://jiyhwfshwvzgom:10aa9f8bce9d36f1271749b82fce10459907a52c80f33f388f995ec36e2bfb4a@ec2-174-129-253-104.compute-1.amazonaws.com:5432/db3r8ta6ni6o1n')
        self.db = "dbname={} user={} password={} host={} ".format(url.path[1:], url.username, url.password, url.hostname)

    def get_certificate(self, email):
        query = f'SELECT * FROM CERTIFICATE WHERE username = "{email}";'

        with psycopg2.connect(self.db) as conn:
            conn.cursor().execute(query)

            resp = conn.cursor().fetchone()
            if not resp:
                return None

            return self.create_certificate(resp)

    def get_certificates(self):
        query = f'SELECT * FROM CERTIFICATE;'

        with psycopg2.connect(self.db) as conn:
            conn.cursor().execute(query)

            try:
                certificates = conn.cursor().fetchall()
                certificates_objects = []
                for certificate in certificates:
                    certificates_objects.append(self.create_certificate(certificate))

                return certificates_objects

            except psycopg2.ProgrammingError:
                return []

    def generate_certificate(self, username, team_name, date):
        query = f'INSERT INTO CERTIFICATE (username, team_name, generation_date) VALUES ("{username}", "{team_name}", "{date}");'

        with psycopg2.connect(self.db) as conn:
            try:
                conn.cursor().execute(query)
                return True

            except psycopg2.IntegrityError:
                return False

    def create_certificate(self, query_result):
        if not query_result:
            return None

        return Certificate(*query_result[1:])


if __name__ == '__main__':
    c = CertificatesDB()
    print(c.get_certificates())