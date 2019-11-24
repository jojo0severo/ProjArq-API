import json
import secrets
from flask import Flask, request, jsonify
from server_helper.api_manager import Manager
from flask_socketio import SocketIO

key = secrets.token_urlsafe(16)

app = Flask(__name__)
socket = SocketIO(app)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = key
manager = Manager()


@app.route('/login', methods=['POST'])
def login():
    response = {'data': {}, 'message': 'Error'}

    try:
        data = request.get_json()

        username = data['username']
        password = data['password']
        is_student = data['is_student']

        if manager.check_user(username, password, is_student):
            response['data'] = manager.get_user(username, username.endswith('@acad.pucrs.br'))
            response['message'] = 'Logged'
            status_code = 200

        else:
            status_code = 401
            response['message'] = 'User not registered'

    except json.JSONDecodeError:
        status_code = 415
        response['message'] = 'Wrong message format'

    except KeyError:
        status_code = 400
        response['message'] = 'Wrong keys sent'

    except TypeError:
        status_code = 400
        response['message'] = 'Wrong values type sent'
        
    except Exception as e:
        status_code = 500
        response['message'] = 'Exception: ' + str(e)
        
    return jsonify(response), status_code


@app.route('/avaliadores', methods=['POST'])
def register_valuer():
    response = {'data': {}, 'message': 'Error'}

    try:
        data = request.get_json()

        username = data['username']
        password = data['password']

        if manager.add_valuer(username, password):
            response['data'] = manager.get_user(username, False)
            response['message'] = 'Registered'
            status_code = 201

        else:
            status_code = 401
            response['message'] = 'Valuer could not be registered'

    except json.JSONDecodeError:
        status_code = 415
        response['message'] = 'Wrong message format'

    except KeyError:
        status_code = 400
        response['message'] = 'Wrong keys sent'

    except TypeError:
        status_code = 400
        response['message'] = 'Wrong values type sent'

    return jsonify(response), status_code


@app.route('/avaliadores/avaliar', methods=['POST'])
def rate_team():
    response = {'data': {}, 'message': 'Error'}

    try:
        data = request.get_json()
        valuer_name = data['valuer']
        team_name = data['team_name']
        software = data['software']
        pitch = data['pitch']
        innovation = data['innovation']
        team = data['team']

        if manager.rate_team(valuer_name, team_name, software, pitch, innovation, team):
            response['message'] = 'Team rated'
            status_code = 204
            socket.emit('team_rated', data={'team_name': team_name}, broadcast=True)

        else:
            status_code = 401
            response['message'] = 'Team could not be rated'

    except json.JSONDecodeError:
        status_code = 415
        response['message'] = 'Wrong message format'

    except KeyError:
        status_code = 400
        response['message'] = 'Wrong keys sent'

    except TypeError:
        status_code = 400
        response['message'] = 'Wrong values type sent'

    return jsonify(response), status_code


@app.route('/equipes', methods=['GET'])
def get_teams():
    response = {'data': manager.get_teams(), 'message': 'Ok'}
    status_code = 200

    return jsonify(response), status_code


@app.route('/equipes/<team_name>', methods=['GET'])
def get_team(team_name):
    response = {'data': {}, 'message': 'Error'}

    team = manager.get_team(team_name)
    if not team:
        status_code = 404
        response['message'] = 'Team not found'
    else:
        response['data'] = team
        response['message'] = 'Ok'
        status_code = 200

    return jsonify(response), status_code


@app.route('/equipes/equipe', methods=['POST'])
def create_team():
    response = {'data': {}, 'message': 'Error'}

    try:
        data = request.get_json()
        team_name = data['team_name']
        admin_email = data['username']

        if manager.add_team(team_name, admin_email):
            response['message'] = 'Team created'
            status_code = 201
            socket.emit('team_created', data={'team': manager.get_team(team_name)}, broadcast=True)

        else:
            status_code = 401
            response['message'] = 'Team could not be created'

    except json.JSONDecodeError:
        status_code = 415
        response['message'] = 'Wrong message format'

    except KeyError:
        status_code = 400
        response['message'] = 'Wrong keys sent'

    except TypeError:
        status_code = 400
        response['message'] = 'Wrong values type sent'

    return jsonify(response), status_code


@app.route('/equipes/equipe', methods=['DELETE'])
def delete_team():
    response = {'data': {}, 'message': 'Error'}

    try:
        data = request.get_json()
        team_name = data['team_name']
        admin_email = data['username']

        if manager.delete_team(team_name, admin_email):
            response['message'] = 'Team deleted'
            status_code = 204
            socket.emit('team_deleted', data={'team': team_name}, broadcast=True)

        else:
            status_code = 401
            response['message'] = 'Team could not be deleted'

    except json.JSONDecodeError:
        status_code = 415
        response['message'] = 'Wrong message format'

    except KeyError:
        status_code = 400
        response['message'] = 'Wrong keys sent'

    except TypeError:
        status_code = 400
        response['message'] = 'Wrong values type sent'

    return jsonify(response), status_code


@app.route('/equipes/equipe/team', methods=['PUT'])
def edit_team_add_members():
    response = {'data': {}, 'message': 'Error'}

    try:
        data = request.get_json()

        team_name = data['team_name']
        admin_email = data['username']
        members = data['members']

        if manager.add_members(team_name, admin_email, members):
            response['message'] = 'Members added'
            status_code = 204
            socket.emit('member_added', data={'team': manager.get_team(team_name)}, broadcast=True)

        else:
            status_code = 401
            response['message'] = 'Members could not be added'

    except json.JSONDecodeError:
        status_code = 415
        response['message'] = 'Wrong message format'

    except KeyError:
        status_code = 400
        response['message'] = 'Wrong keys sent'

    except TypeError:
        status_code = 400
        response['message'] = 'Wrong values type sent'

    return jsonify(response), status_code


@app.route('/equipes/equipe/team', methods=['DELETE'])
def edit_team_remove_members():
    response = {'data': {}, 'message': 'Error'}

    try:
        data = request.get_json()

        team_name = data['team_name']
        admin_email = data['username']
        members = data['members']

        if manager.delete_members(team_name, admin_email, members):
            response['message'] = 'Members removed'
            status_code = 204
            socket.emit('member_removed', data={'team': manager.get_team(team_name)}, broadcast=True)

        else:
            status_code = 401
            response['message'] = 'Members could not be deleted'

    except json.JSONDecodeError:
        status_code = 415
        response['message'] = 'Wrong message format'

    except KeyError:
        status_code = 400
        response['message'] = 'Wrong keys sent'

    except TypeError:
        status_code = 400
        response['message'] = 'Wrong values type sent'

    return jsonify(response), status_code


@app.route('/equipes/equipe/me', methods=['PUT'])
def enter_team():
    response = {'data': {}, 'message': 'Error'}

    try:
        data = request.get_json()

        team_name = data['team_name']
        email = data['username']

        if manager.add_member(team_name, email):
            response['data'] = manager.get_user(email, True).json()
            response['message'] = 'User added'
            status_code = 200
            socket.emit('member_added', data={'team': manager.get_team(team_name)}, broadcast=True)

        else:
            status_code = 401
            response['message'] = 'User could not be added to team'

    except json.JSONDecodeError:
        status_code = 415
        response['message'] = 'Wrong message format'

    except KeyError:
        status_code = 400
        response['message'] = 'Wrong keys sent'

    except TypeError:
        status_code = 400
        response['message'] = 'Wrong values type sent'

    return jsonify(response), status_code


@app.route('/equipes/equipe/me', methods=['DELETE'])
def leave_team():
    response = {'data': {}, 'message': 'Error'}

    try:
        data = request.get_json()

        team_name = data['team_name']
        email = data['username']

        if manager.delete_member(team_name, email):
            response['data'] = manager.get_user(email, True)
            response['message'] = 'User removed'
            status_code = 200
            socket.emit('member_removed', data={'team': manager.get_team(team_name)}, broadcast=True)

        else:
            status_code = 401
            response['message'] = 'User could not be removed from team'

    except json.JSONDecodeError:
        status_code = 415
        response['message'] = 'Wrong message format'

    except KeyError:
        status_code = 400
        response['message'] = 'Wrong keys sent'

    except TypeError:
        status_code = 400
        response['message'] = 'Wrong values type sent'

    return jsonify(response), status_code


@app.route('/equipes/rank', methods=['GET'])
def teams_rank():
    response = {'data': manager.get_teams_rank(), 'message': 'Ok'}
    status_code = 200

    return jsonify(response), status_code


@app.route('/certificates', methods=['GET'])
def get_certificates():
    response = {'data': {}, 'message': 'Error'}

    try:
        data = request.get_json()

        valuer_name = data['valuer']

        certificates = manager.get_certificates(valuer_name)

        if not certificates:
            status_code = 404
            response['message'] = 'Valuer or certificates not found'

        else:
            response['data'] = certificates
            response['message'] = 'Ok'
            status_code = 200

    except json.JSONDecodeError:
        status_code = 415
        response['message'] = 'Wrong message format'

    except KeyError:
        status_code = 400
        response['message'] = 'Wrong keys sent'

    except TypeError:
        status_code = 400
        response['message'] = 'Wrong values type sent'

    return jsonify(response), status_code


@app.route('/certificates/<student_name>', methods=['GET'])
def get_certificate(student_name):
    response = {'data': {}, 'message': 'Error'}

    try:
        data = request.get_json()

        valuer_name = data['valuer']

        certificate = manager.get_certificate(valuer_name, student_name)

        if not certificate:
            status_code = 404
            response['message'] = 'Valuer or certificate not found'

        else:
            response['data'] = certificate
            response['message'] = 'Ok'
            status_code = 200

    except json.JSONDecodeError:
        status_code = 415
        response['message'] = 'Wrong message format'

    except KeyError:
        status_code = 400
        response['message'] = 'Wrong keys sent'

    except TypeError:
        status_code = 400
        response['message'] = 'Wrong values type sent'

    return jsonify(response), status_code


@app.route('/certificates/<student_name>', methods=['POST'])
def generate_certificate(student_name):
    response = {'data': {}, 'message': 'Error'}

    try:
        data = request.get_json()

        valuer_name = data['valuer']

        if not manager.generate_certificate(valuer_name, student_name):
            status_code = 401
            response['message'] = 'Certificate could not be created'

        else:
            response['message'] = 'Certificate created'
            status_code = 201

    except json.JSONDecodeError:
        status_code = 415
        response['message'] = 'Wrong message format'

    except KeyError:
        status_code = 400
        response['message'] = 'Wrong keys sent'

    except TypeError:
        status_code = 400
        response['message'] = 'Wrong values type sent'

    return jsonify(response), status_code


def check_key(external_key):
    if len(external_key) != len(key):
        return False

    for external_letter, internal_letter in zip(external_key, key):
        if external_letter != internal_letter:
            return False

    return True


if __name__ == '__main__':
    socket.run(app)
