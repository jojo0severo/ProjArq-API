import os
import psycopg2
from urllib.parse import urlparse
from model.team import Team


class TeamsDB:
    def __init__(self):
        url = urlparse(os.environ.get('DATABASE_URL'))
        url = urlparse(
            'postgres://jiyhwfshwvzgom:10aa9f8bce9d36f1271749b82fce10459907a52c80f33f388f995ec36e2bfb4a@ec2-174-129-253-104.compute-1.amazonaws.com:5432/db3r8ta6ni6o1n')
        self.db = "dbname={} user={} password={} host={} ".format(url.path[1:], url.username, url.password, url.hostname)

    def add_team(self, team_name, admin_email):
        first_query = f'INSERT INTO TEAM VALUES ("{team_name}", "{admin_email}", 0.0);'
        second_query = f'INSERT INTO STUDENT_TEAM VALUES ("{team_name}", "{admin_email}");'

        with psycopg2.connect(self.db) as conn:
            try:
                conn.cursor().execute(first_query)
                conn.cursor().execute(second_query)
                return True

            except psycopg2.IntegrityError:
                return False

            except psycopg2.OperationalError:
                return False

    def add_member(self, team_name, member):
        query = f'INSERT INTO STUDENT_TEAM VALUES ("{team_name}", "{member}");'

        with psycopg2.connect(self.db) as conn:
            try:
                conn.cursor().execute(query)
                return True

            except psycopg2.IntegrityError:
                return False

            except psycopg2.OperationalError:
                return False

    def add_members(self, team_name, members):
        query = f'INSERT INTO STUDENT_TEAM VALUES ("{team_name}", '

        with psycopg2.connect(self.db) as conn:
            error_index = 0
            try:
                for member in members:
                    conn.cursor().execute(query + f'"{member}");')
                    error_index += 1

                return True

            except psycopg2.IntegrityError:
                query = f'DELETE FROM STUDENT_TEAM WHERE team_name = "{team_name}" AND email = '

                for member in members[:error_index]:
                    conn.cursor().execute(query + f'"{member}";')

                return False

            except psycopg2.OperationalError:
                query = f'DELETE FROM STUDENT_TEAM WHERE team_name = "{team_name}" AND email = '

                for member in members[:error_index]:
                    conn.cursor().execute(query + f'"{member}";')

                return False

    def get_user_team(self, email):
        query = f'SELECT * FROM STUDENT_TEAM WHERE email = "{email}";'

        with psycopg2.connect(self.db) as conn:
            return self.create_team(conn.cursor().execute(query).fetchall()[0], [])

    def get_team(self, team_name):
        first_query = f'SELECT * FROM TEAM WHERE team_name = "{team_name}";'
        second_query = f'SELECT * FROM STUDENT_TEAM WHERE team_name = "{team_name}";'
        third_query = 'SELECT * FROM STUDENT WHERE email = "'

        with psycopg2.connect(self.db) as conn:
            try:
                conn.cursor().execute(first_query)

                team = conn.cursor().fetchone()
                if not team:
                    return None

                conn.cursor().execute(second_query)

                members = conn.cursor().fetchall()
                full_members = []
                for _, member in members:
                    conn.cursor().execute(third_query + str(member) + '";')
                    full_members.append(conn.cursor().fetchone())

                return self.create_team(team, full_members)

            except psycopg2.ProgrammingError:
                return None

    def get_teams(self):
        query = f'SELECT * FROM TEAM;'
        second_query = 'SELECT * FROM STUDENT WHERE email = "'

        with psycopg2.connect(self.db) as conn:
            try:
                conn.cursor().execute(query)

                teams = conn.cursor().fetchall()
                teams_objects = []
                for team_name, admin_name, rank in teams:
                    conn.cursor().execute(f'SELECT * FROM STUDENT_TEAM WHERE team_name = "{team_name}";')

                    members = conn.cursor().fetchall()
                    full_members = []
                    for _, member in members:
                        conn.cursor().execute(second_query + str(member) + '";')

                        full_members.append(conn.curosr().fetchone())

                    teams_objects.append(self.create_team((team_name, admin_name, rank), full_members))

                return teams_objects

            except psycopg2.ProgrammingError:
                return []

    def get_rank(self):
        query = f'SELECT * FROM TEAM ORDER BY rate DESC;'

        with psycopg2.connect(self.db) as conn:
            try:
                conn.cursor().execute(query)

                teams = conn.cursor().fetchall()
                teams_objects = []
                for team in teams:
                    teams_objects.append(self.create_team(team, []))

                return teams_objects

            except psycopg2.ProgrammingError:
                return []

    def update_rank(self, team_name, rank):
        query = f'UPDATE TEAM SET rate = {float(rank)} WHERE team_name = "{team_name}";'

        with psycopg2.connect(self.db) as conn:
            try:
                conn.cursor().execute(query)
                return True

            except psycopg2.IntegrityError:
                return False

            except psycopg2.OperationalError:
                return False

    def remove_team(self, team_name):
        first_query = f'DELETE FROM STUDENT_TEAM WHERE team_name = "{team_name}";'
        second_query = f'DELETE FROM TEAM WHERE team_name = "{team_name}";'

        with psycopg2.connect(self.db) as conn:
            try:
                conn.cursor().execute(first_query)
                conn.cursor().execute(second_query)
                return True

            except psycopg2.IntegrityError:
                return False

            except psycopg2.OperationalError:
                return False

    def remove_member(self, team_name, member):
        query = f'DELETE FROM STUDENT_TEAM WHERE team_name = "{team_name}" AND email = "{member}";'

        with psycopg2.connect(self.db) as conn:
            try:
                conn.cursor().execute(query)
                return True

            except psycopg2.IntegrityError:
                return False

            except psycopg2.OperationalError:
                return False

    def remove_members(self, team_name, members):
        query = f'DELETE FROM STUDENT_TEAM WHERE team_name = "{team_name}" AND email = '

        with psycopg2.connect(self.db) as conn:
            error_index = 0
            try:
                for member in members:
                    conn.cursor().execute(query + f'"{member}";')
                    error_index += 1

                return True

            except psycopg2.IntegrityError:
                query = f'INSERT INTO STUDENT_TEAM VALUES("{team_name}", '

                for member in members[:error_index]:
                    conn.cursor().execute(query + f'"{member}");')

                return False

            except psycopg2.OperationalError:
                query = f'INSERT INTO STUDENT_TEAM VALUES("{team_name}", '

                for member in members[:error_index]:
                    conn.cursor().execute(query + f'"{member}");')

                return False

    def create_team(self, team, members):
        if not team:
            return None

        t = Team(*team[:2])
        t.add_members([[member, course, email] for member, _, course, email in members])

        return t
