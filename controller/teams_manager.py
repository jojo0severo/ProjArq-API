from model.team import Team
from model.teams_database import TeamsDB


class TeamsManager:
    def __init__(self):
        self.teams = {}
        self.teams_db = TeamsDB()

    def add_team(self, team_name, admin_email):
        if team_name not in self.teams.keys():
            if self.teams_db.add_team(team_name, admin_email):
                self.teams[team_name] = Team(team_name, admin_email)
                return True

        return False

    def add_member(self, team_name, member):
        if team_name in self.teams.keys():
            self.teams[team_name].add_member(member)

        return self.teams_db.add_member(team_name, member)

    def add_members(self, team_name, admin_email, members):
        if team_name in self.teams.keys():
            if admin_email == self.teams[team_name].admin_email:
                if self.teams_db.add_members(team_name, members):
                    self.teams[team_name].add_members(members)
                    return True

            return False

        else:
            team = self.teams_db.get_team(team_name)
            if team is not None and team.admin_email == admin_email:
                self.teams[team_name] = team
                if self.teams_db.add_members(team_name, members):
                    self.teams[team_name].add_members(members)
                    return True

            return False

    def get_user_team(self, username):
        team = self.teams_db.get_user_team(username)
        if team.team_name not in self.teams.keys():
            self.teams[team.team_name] = team

        return team

    def get_team(self, team_name):
        if team_name not in self.teams.keys():
            team = self.teams_db.get_team(team_name)
            if team_name is not None:
                self.teams[team_name] = team

            return team

        return self.teams[team_name]

    def get_teams(self):
        return self.teams_db.get_teams()

    def get_rank(self):
        return self.teams_db.get_rank()

    def update_rank(self, team_name, *args):
        new_rank = sum(args)
        return self.teams_db.update_rank(team_name, new_rank)

    def delete_team(self, team_name, admin_email):
        if team_name in self.teams.keys():
            if self.teams[team_name].admin_email == admin_email and len(self.teams[team_name].members) == 1:
                del self.teams[team_name]
                return self.teams_db.remove_team(team_name)

            return False

        else:
            team = self.teams_db.get_team(team_name)
            if team is not None and team.admin_email == admin_email and len(team.members) == 1:
                return self.teams_db.remove_team(team_name)

            return False

    def delete_member(self, team_name, member):
        if team_name in self.teams.keys():
            if self.teams[team_name].admin_email == member:
                return False

            self.teams[team_name].remove_member(member)
            return self.teams_db.remove_member(team_name, member)

        else:
            team = self.teams_db.get_team(team_name)
            if team is not None and team.admin_email != member:
                result = self.teams_db.remove_member(team_name, member)
                self.teams[team_name] = team
                return result

        return False

    def delete_members(self, team_name, admin_email, members):
        if team_name in self.teams.keys():
            if self.teams[team_name].admin_email == admin_email:
                if admin_email in members:
                    return False

                self.teams[team_name].remove_members(members)
                return self.teams_db.remove_members(team_name, members)

            return False

        else:
            team = self.teams_db.get_team(team_name)
            if team is not None and team.admin_email == admin_email and admin_email not in team.members:
                return self.teams_db.remove_members(team_name, members)

            return False
