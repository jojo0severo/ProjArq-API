import sys
import getpass
from messenger import Client


class InterfaceTerminal:
    def __init__(self, url):
        self.c = Client(url)
        self.options = self.set_options()

    def set_options(self):
        return ['Sair', 'Login', 'Criar avaliador', 'Avaliar time', 'Listar times', 'Ver time', 'Criar time', 'Deletar time',
                'Adicionar membros', 'Deletar membros', 'Entrar no time', 'Sair do time', 'Listar rank',
                'Listar certificados', 'Ver certificado', 'Gerar certificado']

    def loop(self):
        out = False

        while not out:
            for idx, option in enumerate(self.options):
                print(str(idx) + ' - ' + option)
            
            print('\n')
            choice = int(input('Qual das opções deseja tentar?\n'))
            print('\n')

            if choice == 0:
                self.c.disconnect()
                break

            elif choice == 1:
                is_student = True if int(input('Deseja entrar como avaliador ou estudante? (0 ou 1)\n')) == 1 else 0
                print()
                username = input('Informe um nome de usuario valido\n')
                print()
                password = getpass.getpass(prompt='Informe sua senha\n')
                print()

                self.c.login(username, password, is_student)

            elif choice == 2:
                username = input('Informe um nome de usuario\n')
                print()
                password = getpass.getpass(prompt='Informe uma senha\n')
                print()

                self.c.create_valuer(username, password)

            elif choice == 3:
                valuer_name = input('Informe o seu nome de usuario\n')
                print()
                team_name = input('Informe o nome do time a ser avaliado\n')
                print()
                software = int(input('De uma nota para a qualidade de software (inteiro)\n'))
                print()
                pitch = int(input('De uma nota para a qualidade do pitch (inteiro)\n'))
                print()
                innovation = int(input('De uma nota para o grau de inovacao do time (inteiro)\n'))
                print()
                team = int(input('De uma nota para o time (inteiro)\n'))
                print()

                self.c.rate_team(valuer_name, team_name, software, pitch, innovation, team)

            elif choice == 4:
                self.c.get_teams()

            elif choice == 5:
                team_name = input('Informe o nome do time\n')
                print()

                self.c.get_team(team_name)

            elif choice == 6:
                username = input('Informe seu nome de usuario\n')
                print()
                team_name = input('Informe o nome do time\n')
                print()

                self.c.create_team(team_name, username)

            elif choice == 7:
                username = input('Informe seu nome de usuario\n')
                print()
                team_name = input('Informe o nome do time\n')
                print()

                self.c.delete_team(team_name, username)

            elif choice == 8:
                username = input('Informe seu nome de usuario\n')
                print()
                team_name = input('Informe o nome do time\n')
                print()
                members = []
                member = input('Informe o nome do novo membro do time\n')
                print()
                members.append(member)
                while 1:
                    member = input('Informe o nome do novo membro do time\n')
                    print()
                    if not member:
                        break
                    members.append(member)

                self.c.add_members_to_team(team_name, username, members)

            elif choice == 9:
                username = input('Informe seu nome de usuario\n')
                print()
                team_name = input('Informe o nome do time\n')
                print()
                members = []
                member = input('Informe o nome membro a ser removido do time\n')
                print()
                members.append(member)
                while 1:
                    member = input('Informe o nome membro a ser removido do time\n')
                    print()
                    if not member:
                        break
                    members.append(member)

                self.c.delete_members_from_team(team_name, username, members)

            elif choice == 10:
                username = input('Informe seu nome de usuario\n')
                print()
                team_name = input('Informe o nome do time que deseja entrar\n')
                print()

                self.c.enter_team(team_name, username)

            elif choice == 11:
                username = input('Informe seu nome de usuario\n')
                print()
                team_name = input('Informe o nome do time que deseja entrar\n')
                print()

                self.c.leave_team(team_name, username)

            elif choice == 12:
                self.c.get_teams_rank()

            elif choice == 13:
                username = input('Informe seu nome de usuario\n')
                print()

                self.c.get_certificates(username)

            elif choice == 14:
                username = input('Informe seu nome de usuario\n')
                print()
                student = input('Informe o nome do aluno\n')
                print()

                self.c.get_certificate(username, student)

            elif choice == 15:
                username = input('Informe seu nome de usuario\n')
                print()
                student = input('Informe o nome do aluno\n')
                print()

                self.c.get_certificate(username, student)


if __name__ == '__main__':
    url = sys.argv[1]
    i = InterfaceTerminal(url)
    i.loop()
