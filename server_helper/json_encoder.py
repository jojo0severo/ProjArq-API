import copy


class Encoder:
    def encode_team(self, team):
        team = copy.deepcopy(team)
        if team is None:
            return {}

        return {
            'name': team.team_name,
            'admin_name': team.admin_email,
            'members': team.members
        }

    def encode_teams(self, teams):
        teams = copy.deepcopy(teams)
        return [self.encode_team(team) for team in teams]

    def encode_certificate(self, certificate):
        certificate = copy.deepcopy(certificate)
        if certificate is None:
            return {}

        return {
            'student_name': certificate.student_name,
            'team_name': certificate.team_name,
            'generation_date': certificate.generation_date
        }

    def encode_certificates(self, certificates):
        certificates = copy.deepcopy(certificates)
        return [self.encode_certificate(certificate) for certificate in certificates]
