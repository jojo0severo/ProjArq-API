import sqlite3
from model.certificate import Certificate


class CertificatesDB:
    def get_certificate(self, username):
        query = f'SELECT * FROM CERTIFICATE WHERE username = "{username}";'

        with sqlite3.connect('database/local.db') as conn:
            resp = conn.cursor().execute(query).fetchall()
            if not resp:
                return None

            return self.create_certificate(resp[0])

    def get_certificates(self):
        query = f'SELECT * FROM CERTIFICATE;'

        with sqlite3.connect('database/local.db') as conn:
            certificates = conn.cursor().execute(query).fetchall()
            certificates_objects = []
            for certificate in certificates:
                certificates_objects.append(self.create_certificate(certificate))

            return certificates_objects

    def generate_certificate(self, username, team_name, date):
        query = f'INSERT INTO CERTIFICATE (username, team_name, generation_date) VALUES ("{username}", "{team_name}", "{date}");'

        with sqlite3.connect('database/local.db') as conn:
            try:
                conn.cursor().execute(query)
                return True


            except sqlite3.IntegrityError:
                return False

    def create_certificate(self, query_result):
        if not query_result:
            return None

        return Certificate(*query_result[1:])
