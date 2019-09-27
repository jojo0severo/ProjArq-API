import json
import time
import socketio
import requests


class Client:
    def __init__(self, url):
        self.url = url
        self.socket = socketio.Client()
        self.socket.connect(url)
        self.define_callbacks()
        self.wait_timeout = True

        print('Batata - Jequiti\n\n\n\n\n\n')
        time.sleep(0.3)

        with open('ascii1.txt', 'r') as file1:
            print(file1.read())

        time.sleep(4)

        with open('ascii2.txt', 'r') as file2:
            print(file2.read())

        time.sleep(3)

    def define_callbacks(self):
        self.socket.on('team_rated', self.get_response)
        self.socket.on('team_created', self.get_response)
        self.socket.on('team_deleted', self.get_response)
        self.socket.on('member_added', self.get_response)
        self.socket.on('member_removed', self.get_response)

    def get_response(self, *args):
        while self.wait_timeout:
            pass

        print('Socket response:', args)
        self.wait_timeout = True

    def login(self, username, password, is_student):
        print('\nDoing login\n')

        resp = requests.post(self.url + 'login',
                             json={'username': username, 'password': password, 'is_student': is_student})

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not login with these information. Status:', resp.status_code)
            print('Sabiam que o plural de "information" eh "information"?')

        print()
        time.sleep(3)

    def create_valuer(self, username, password):
        print('\nCreating valuer\n')

        resp = requests.post(self.url + 'avaliadores', json={'username': username, 'password': password})

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not create valuer with these information. Status:', resp.status_code)

        print()
        time.sleep(3)

    def rate_team(self, valuer_name, team_name, software, pitch, innovation, team):
        print('\nRating team\n')

        resp = requests.post(self.url + 'avaliadores/avaliar',
                             json={
                                 'valuer': valuer_name,
                                 'team_name': team_name,
                                 'software': software,
                                 'pitch': pitch,
                                 'innovation': innovation,
                                 'team': team
                             })

        print(5, end='', flush=True)
        time.sleep(1)
        for i in range(4, 0, -1):
            print('\b' + str(i), end='', flush=True)
            time.sleep(1)
        print('\b', end='', flush=True)
        print('\b', end='', flush=True)

        time.sleep(0.5)

        self.wait_timeout = False

        time.sleep(0.5)

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not rate team. Status:', resp.status_code)

        print()
        time.sleep(3)

    def get_teams(self):
        print('\nGetting teams\n')

        resp = requests.get(self.url + 'equipes')

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not retrieve the teams. Status:', resp.status_code)

        print()
        time.sleep(3)

    def get_team(self, team_name):
        print('\nGetting team\n')

        resp = requests.get(self.url + 'equipes/' + str(team_name))

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not retrieve team. Status:', resp.status_code)

        print()
        time.sleep(3)

    def create_team(self, team_name, username):
        print('\nCreating team\n')

        resp = requests.post(self.url + 'equipes/equipe', json={'team_name': team_name, 'username': username})

        print(5, end='', flush=True)
        time.sleep(1)
        for i in range(4, 0, -1):
            print('\b' + str(i), end='', flush=True)
            time.sleep(1)
        print('\b', end='', flush=True)
        print('\b', end='', flush=True)

        time.sleep(1)

        self.wait_timeout = False

        time.sleep(1)

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not create team. Status:', resp.status_code)

        print()
        time.sleep(3)

    def delete_team(self, team_name, username):
        print('\nDeleting team\n')

        resp = requests.delete(self.url + 'equipes/equipe', json={'team_name': team_name, 'username': username})

        print(5, end='', flush=True)
        time.sleep(1)
        for i in range(4, 0, -1):
            print('\b' + str(i), end='', flush=True)
            time.sleep(1)
        print('\b', end='', flush=True)
        print('\b', end='', flush=True)

        time.sleep(1)

        self.wait_timeout = False

        time.sleep(1)

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not delete team. Status:', resp.status_code)

        print()
        time.sleep(3)

    def add_members_to_team(self, team_name, username, members_names):
        print('\nAdding members\n')

        resp = requests.put(self.url + 'equipes/equipe/team',
                            json={'team_name': team_name, 'username': username, 'members': members_names})

        print(5, end='', flush=True)
        time.sleep(1)
        for i in range(4, 0, -1):
            print('\b' + str(i), end='', flush=True)
            time.sleep(1)
        print('\b', end='', flush=True)
        print('\b', end='', flush=True)

        time.sleep(1)

        self.wait_timeout = False

        time.sleep(1)

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not add members. Status:', resp.status_code)

        print()
        time.sleep(3)

    def delete_members_from_team(self, team_name, username, members_names):
        print('\nDeleting members\n')

        resp = requests.delete(self.url + 'equipes/equipe/team',
                               json={'team_name': team_name, 'username': username, 'members': members_names})

        print(5, end='', flush=True)
        time.sleep(1)
        for i in range(4, 0, -1):
            print('\b' + str(i), end='', flush=True)
            time.sleep(1)
        print('\b', end='', flush=True)
        print('\b', end='', flush=True)

        time.sleep(1)

        self.wait_timeout = False

        time.sleep(1)

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not delete members from team. Status:', resp.status_code)

        print()
        time.sleep(3)

    def enter_team(self, team_name, username):
        print('\nEntering team\n')

        resp = requests.put(self.url + 'equipes/equipe/me', json={'team_name': team_name, 'username': username})

        print(5, end='', flush=True)
        time.sleep(1)
        for i in range(4, 0, -1):
            print('\b' + str(i), end='', flush=True)
            time.sleep(1)
        print('\b', end='', flush=True)
        print('\b', end='', flush=True)

        time.sleep(1)

        self.wait_timeout = False

        time.sleep(1)

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not enter the team. Status:', resp.status_code)

        print()
        time.sleep(3)

    def leave_team(self, team_name, username):
        print('\nLeaving team\n')

        resp = requests.delete(self.url + 'equipes/equipe/me', json={'team_name': team_name, 'username': username})

        print(5, end='', flush=True)
        time.sleep(1)
        for i in range(4, 0, -1):
            print('\b' + str(i), end='', flush=True)
            time.sleep(1)
        print('\b', end='', flush=True)
        print('\b', end='', flush=True)

        time.sleep(1)

        self.wait_timeout = False

        time.sleep(1)

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not leave team. Status:', resp.status_code)

        print()
        time.sleep(3)

    def get_teams_rank(self):
        print('\nGetting rank\n')

        resp = requests.get(self.url + 'equipes/rank')

        print(5, end='', flush=True)
        time.sleep(1)
        for i in range(4, 0, -1):
            print('\b' + str(i), end='', flush=True)
            time.sleep(1)
        print('\b', end='', flush=True)
        print('\b', end='', flush=True)

        time.sleep(1)

        self.wait_timeout = False

        time.sleep(1)

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not get the rank of the teams. Status:', resp.status_code)

        print()
        time.sleep(3)

    def get_certificates(self, valuer_name):
        print('\nGetting certificates\n')

        resp = requests.get(self.url + 'certificates', json={'valuer': valuer_name})

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not retrieve the certificates. Status:', resp.status_code)

        print()
        time.sleep(3)

    def get_certificate(self, valuer_name, student_name):
        print('\nGetting certificate\n')

        resp = requests.get(self.url + 'certificates/' + str(student_name), json={'valuer': valuer_name})

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not retrieve the student certificate. Status:', resp.status_code)

        print()
        time.sleep(3)

    def generate_certificate(self, valuer_name, student_name):
        print('\nGenerating certificate\n')

        resp = requests.post(self.url + 'certificates/' + str(student_name), json={'valuer': valuer_name})

        if resp:
            print('HTTP response:', json.dumps(resp.json(), indent=4))
        else:
            print('Could not generate a certificate. Status:', resp.status_code)

        print()
        time.sleep(3)


