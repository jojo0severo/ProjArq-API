from controller.users_manager import UsersManager
from controller.teams_manager import TeamsManager
from controller.certificates_manager import CertificatesManager
from server_helper.json_encoder import Encoder


class Manager:
    def __init__(self):
        self.users_manager = UsersManager()
        self.teams_manager = TeamsManager()
        self.certificates_manager = CertificatesManager()
        self.json_encoder = Encoder()

    def get_user(self, username, is_student):
        return self.json_encoder.encode_user(self.users_manager.get_user(username, is_student), is_student)

    def add_student(self, username, password, course, email):
        return self.users_manager.add_user(username, password, True, course, email)

    def add_valuer(self, username, password):
        return self.users_manager.add_user(username, password, False, '', '')

    def check_user(self, username, password, is_student):
        return self.users_manager.check_user(username, password, is_student)

    def add_team(self, team_name, admin_email):
        return self.teams_manager.add_team(team_name, admin_email)

    def add_member(self, team_name, member):
        team = self.teams_manager.get_team(team_name)

        if team is None:
            return False

        if len(team.members) == 6:
            return False

        es_counter = 0
        for member, course in team.members:
            if course == 'ES':
                es_counter += 1
                if es_counter == 4:
                    return False

        return self.teams_manager.add_member(team_name, member)

    def add_members(self, team_name, admin_email, members):
        team = self.teams_manager.get_team(team_name)

        if team is None:
            return False

        if len(team.members) == 6:
            return False

        es_counter = 0
        for member, course in team.members:
            if course == 'ES':
                es_counter += 1

            if es_counter == 4:
                return False

        for member in members:
            student = self.users_manager.get_user(member, True)
            if student is None:
                return False

            if student.course == 'ES':
                es_counter += 1
                if es_counter > 4:
                    return False

        return self.teams_manager.add_members(team_name, admin_email, members)

    def get_team(self, team_name):
        return self.json_encoder.encode_team(self.teams_manager.get_team(team_name))

    def get_teams(self):
        return self.json_encoder.encode_teams(self.teams_manager.get_teams())

    def delete_team(self, team_name, admin_email):
        return self.teams_manager.delete_team(team_name, admin_email)

    def delete_member(self, team_name, member):
        return self.teams_manager.delete_member(team_name, member)

    def delete_members(self, team_name, admin_email, members):
        return self.teams_manager.delete_members(team_name, admin_email, members)

    def get_teams_rank(self):
        return self.json_encoder.encode_teams(self.teams_manager.get_rank())

    def rate_team(self, valuer_name, team_name, software, pitch, innovation, team):
        valuer = self.users_manager.get_user(valuer_name, False)
        if valuer is None:
            return False

        return self.teams_manager.update_rank(team_name, software, pitch, innovation, team)

    def get_certificate(self, valuer_name, student_email):
        valuer = self.users_manager.get_user(valuer_name, False)
        if valuer is None:
            return None

        return self.json_encoder.encode_certificate(self.certificates_manager.get_certificate(student_email))

    def get_certificates(self, valuer_name):
        valuer = self.users_manager.get_user(valuer_name, False)
        if valuer is None:
            return []

        return self.json_encoder.encode_certificates(self.certificates_manager.get_certificates())

    def generate_certificate(self, valuer_name, student_name):
        valuer = self.users_manager.get_user(valuer_name, False)
        if valuer is None:
            return False

        team = self.teams_manager.get_user_team(student_name)
        if team is None:
            return False

        return self.certificates_manager.generate_certificate(student_name, team.team_name)
