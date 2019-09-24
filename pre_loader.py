import random
import requests
from server_helper.api_manager import Manager


def generate_students():
    courses = ['ES', 'SI', 'CC', 'EC']
    names = requests.get('http://www.wjr.eti.br/nameGenerator/index.php?q=220&o=json').json()
    with open('resources/students.csv', 'w') as stud:
        for i in range(100):
            registration = random.randint(16103100, 18103900)
            course = random.choice(courses)
            name = random.choice(names)
            stud.write(str(name) + ',' + str(registration) + ',' + str(course) + '\n')


def load_students():
    manager = Manager()
    with open('resources/students.csv', 'r') as stud:
        lines = stud.read().split('\n')[1:]
        for line in lines:
            name, registration, course = line.split(',')
            manager.add_student(name, registration, course)


if __name__ == '__main__':
    # generate_students()
    load_students()
