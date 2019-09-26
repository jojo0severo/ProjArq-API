import re
import random
import requests
from server_helper.api_manager import Manager

a = '[ãáàâ]'
e = '[éèê]'
i = '[íìî]'
o = '[õóòô]'
u = '[úùû]'


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
    manager = Manager()
    with open('resources/students.csv', 'r', encoding='utf-8') as stud:
        lines = stud.read().split('\n')[:-1]
        for line in lines:
            name, registration, course, email = line.split(',')
            manager.add_student(name, registration, course, email)


if __name__ == '__main__':
    # generate_students()
    load_students()
