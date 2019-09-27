import re
import random
import requests
from server_helper.api_manager import Manager

a = '[ãáàâ]'
e = '[éèê]'
i = '[íìî]'
o = '[õóòô]'
u = '[úùû]'

manager = Manager()


def generate_students():
    courses = ['ES', 'SI', 'CC', 'EC']
    names = requests.get('http://www.wjr.eti.br/nameGenerator/index.php?q=220&o=json').json()
    with open('resources/students.csv', 'w', encoding='utf-8') as stud:
        for _ in range(100):
            registration = random.randint(16103100, 18103900)
            course = random.choice(courses)
            name = random.choice(names)
            email = re.sub(str(a), 'a', name.lower())
            email = re.sub(str(e), 'e', email)
            email = re.sub(str(i), 'i', email)
            email = re.sub(str(o), 'o', email)
            email = re.sub(str(u), 'u', email)
            email = email.replace(' ', '_').replace('ç', 'c') + '@acad.pucrs.br'
            stud.write(str(name) + ',' + str(registration) + ',' + str(course) + ',' + str(email) + '\n')


def load_students():
    with open('resources/students.csv', 'r', encoding='utf-8') as stud:
        lines = stud.read().split('\n')[:-1]
        for line in lines:
            name, registration, course, email = line.split(',')
            manager.add_student(name, registration, course, email)


def load_valuers():
    valuers = [
        ('joao', 'joao'),
        ('pedro', 'pedro'),
        ('maria', 'maria')]

    for name, password in valuers:
        manager.add_valuer(name, password)


def load_teams():
    teams_names = ['team_' + str(j + 1) for j in range(5)]
    teams = []

    with open('resources/students.csv', 'r', encoding='utf-8') as stud:
        lines = stud.read().split('\n')[:-1]

        admins = random.choices(lines, k=5)
        [lines.remove(admin) for admin in admins]

        first_members = random.choices(lines, k=5)
        [lines.remove(member) for member in first_members]

        second_members = random.choices(lines, k=5)
        [lines.remove(member) for member in second_members]

        third_members = random.choices(lines, k=5)
        [lines.remove(member) for member in third_members]

        fourth_members = random.choices(lines, k=5)
        [lines.remove(member) for member in fourth_members]

        fifth_members = random.choices(lines, k=5)

        for j in range(5):
            team_name = teams_names[j]
            _, _, _, admin = admins[j].split(',')
            members = [first_members[j].split(','), second_members[j].split(','), third_members[j].split(','),
                       fourth_members[j].split(','), fifth_members[j].split(',')]

            teams.append({'admin_email': admin, 'team_name': team_name, 'members': members})

    for team in teams:
        manager.add_team(team['team_name'], team['admin_email'])
        members = [email for _, _, _, email in team['members']]
        print(manager.add_members(team['team_name'], team['admin_email'], members))


if __name__ == '__main__':
    # generate_students()
    load_students()
    load_valuers()
    load_teams()
