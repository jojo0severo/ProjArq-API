import os
import psycopg2
from urllib.parse import urlparse
from model.team import Team


class TeamsDB:
    def __init__(self):
        url = urlparse(os.environ.get('DATABASE_URL'))
        self.db = "dbname={} user={} password={} host={} ".format(url.path[1:], url.username, url.password, url.hostname)

    def add_team(self, team_name, admin_email):
        first_query = f'INSERT INTO TEAM (team_name, admin, rate) VALUES (%s, %s, 0.0);'
        second_query = f'INSERT INTO STUDENT_TEAM (team_name, email) VALUES (%s, %s);'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(first_query, (team_name, admin_email))
                    cursor.execute(second_query, (team_name, admin_email))
                    conn.commit()
                    return True

                except psycopg2.IntegrityError:
                    return False

                except psycopg2.OperationalError:
                    return False

    def add_member(self, team_name, member_email):
        query = f'INSERT INTO STUDENT_TEAM (team_name, email) VALUES (%s, %s);'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, (team_name, member_email))
                    conn.commit()
                    return True

                except psycopg2.IntegrityError:
                    return False

                except psycopg2.OperationalError:
                    return False

    def add_members(self, team_name, members):
        query = f'INSERT INTO STUDENT_TEAM (team_name, email) VALUES (%s, %s);'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                error_index = 0
                try:
                    for member in members:
                        cursor.execute(query, (team_name, member))
                        error_index += 1

                    conn.commit()
                    return True

                except psycopg2.IntegrityError:
                    query = f'DELETE FROM STUDENT_TEAM WHERE team_name = %s AND email = %s;'

                    for member in members[:error_index]:
                        cursor.execute(query, (team_name, member))

                    conn.commit()
                    return False

                except psycopg2.OperationalError:
                    query = f'DELETE FROM STUDENT_TEAM WHERE team_name = %s AND email = %s;'

                    for member in members[:error_index]:
                        cursor.execute(query, (team_name, member))

                    conn.commit()
                    return False

    def get_user_team(self, email):
        query = f'SELECT * FROM STUDENT_TEAM WHERE email = %s;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    return self.create_team(cursor.execute(query, (email,)).fetchone(), [])
                except psycopg2.ProgrammingError:
                    return None

    def get_team(self, team_name):
        first_query = f'SELECT * FROM TEAM WHERE team_name = %s;'
        second_query = f'SELECT * FROM STUDENT_TEAM WHERE team_name = %s;'
        third_query = 'SELECT * FROM STUDENT WHERE email = %s;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(first_query, (team_name,))
                    team = cursor.fetchone()
                    if not team:
                        return None

                    cursor.execute(second_query, (team_name,))
                    members = cursor.fetchall()
                    full_members = []
                    for _, member in members:
                        cursor.execute(third_query, (member,))
                        full_members.append(cursor.fetchone())

                    return self.create_team(team, full_members)

                except psycopg2.ProgrammingError:
                    return None

    def get_teams(self):
        query = f'SELECT * FROM TEAM;'
        second_query = 'SELECT * FROM STUDENT WHERE email = %s;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    conn.cursor().execute(query)

                    teams = cursor.fetchall()
                    print("Found team")
                    teams_objects = []
                    for team_name, admin_name, rank in teams:
                        cursor.execute(f'SELECT * FROM STUDENT_TEAM WHERE team_name = %s;', (team_name,))

                        members = cursor.fetchall()
                        print("Found members")
                        full_members = []
                        for _, member in members:
                            print("searching for member:", member)
                            cursor.execute(second_query, (member,))
                            full_members.append(cursor.fetchone())
                            print("Found member")

                        teams_objects.append(self.create_team((team_name, admin_name, rank), full_members))

                    return teams_objects

                except psycopg2.ProgrammingError as e:
                    print("Programming error", str(e))
                    return []

    def get_rank(self):
        query = f'SELECT * FROM TEAM ORDER BY rate DESC;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query)
                    teams = cursor.fetchall()
                    teams_objects = []
                    for team in teams:
                        teams_objects.append(self.create_team(team, []))

                    return teams_objects

                except psycopg2.ProgrammingError:
                    return []

    def update_rank(self, team_name, rank):
        query = f'UPDATE TEAM SET rate = %f WHERE team_name = %s;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, (float(rank), team_name))
                    conn.commit()
                    return True

                except psycopg2.IntegrityError:
                    return False

                except psycopg2.OperationalError:
                    return False

    def remove_team(self, team_name):
        first_query = f'DELETE FROM STUDENT_TEAM WHERE team_name = %s;'
        second_query = f'DELETE FROM TEAM WHERE team_name = %s;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(first_query, (team_name,))
                    cursor.execute(second_query, (team_name,))
                    conn.commit()
                    return True

                except psycopg2.IntegrityError:
                    return False

                except psycopg2.OperationalError:
                    return False

    def remove_member(self, team_name, member_email):
        query = f'DELETE FROM STUDENT_TEAM WHERE team_name = %s AND email = %s;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, (team_name, member_email))
                    conn.commit()
                    return True

                except psycopg2.IntegrityError:
                    return False

                except psycopg2.OperationalError:
                    return False

    def remove_members(self, team_name, members):
        query = f'DELETE FROM STUDENT_TEAM WHERE team_name = %s AND email = %s;'

        with psycopg2.connect(self.db) as conn:
            with conn.cursor() as cursor:
                try:
                    error_index = 0
                    for member in members:
                        cursor.execute(query, (team_name, member))
                        error_index += 1

                    conn.commit()
                    return True

                except psycopg2.IntegrityError:
                    query = f'INSERT INTO STUDENT_TEAM VALUES(%s, %s);'

                    for member in members[:error_index]:
                        cursor.execute(query, (team_name, member))

                    conn.commit()
                    return False

                except psycopg2.OperationalError:
                    query = f'INSERT INTO STUDENT_TEAM VALUES(%s, %s);'

                    for member in members[:error_index]:
                        cursor.execute(query, (team_name, member))

                    conn.commit()
                    return False

    def create_team(self, team, members):
        if not team:
            return None

        t = Team(*team[:2])
        t.add_members([[member, course, email] for member, _, course, email in members])

        return t
