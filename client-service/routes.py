from flask import request, jsonify, Blueprint, g
from models import Client, ClientSchema, db

import requests

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

client_blueprint = Blueprint('client_api_routes', __name__, url_prefix='/')

USER_API_URL = 'http://127.0.0.1:5001/current-user'


def get_user(api_key):
    headers = {
        'Authorization': api_key
    }

    response = requests.get(USER_API_URL, headers=headers)

    if response.status_code != 200:
        return {'message': 'Not Authorized'}

    user = response.json()
    return user


@client_blueprint.route("/clients", methods=["GET"])
def get_clients():
    clients = Client.query.all()
    result = [client.serialize() for client in clients]

    return result


@client_blueprint.route("/clients", methods=["POST"])
def add_client():
    # Check if user is authenticated

    try:
        api_key = request.headers.get('Authorization')


        if not api_key:
            return jsonify({'message': 'Not logged in 1'}), 401
        response = get_user(api_key)

        if not response.get('result'):
            return jsonify({'message': 'Not logged in 2'}), 401

        client = Client()
        user = response.get('result')
        client.user_id = user['id']
        client.contact_name = request.json.get('contact_name')
        client.contact_number = request.json.get('contact_number')
        contact_email = request.json.get('contact_email')

        check_email = Client.query.filter_by(contact_email=contact_email).first()

        if check_email:
            return jsonify({'message': 'client with this email already exist'})

        client.contact_email = contact_email

        db.session.add(client)
        db.session.commit()

        response = {
            "message": "Client added",
            "result": client.serialize()
        }
    except:
        response = {"message": "error in adding the client"}

    return response


@client_blueprint.route("/clients/<id>", methods=["GET"])
def get_client(id):
    client = Client.query.get(id)
    if not client:
        return jsonify({"message": "client does not exist"})
    return client.serialize()


@client_blueprint.route("/clients/<id>", methods=["PUT"])
def update_client(id):
    # Check if user is authenticated
    client = Client.query.get(id)
    if not client:
        return jsonify({"message": "client does not exist"})

    api_key = request.headers.get('Authorization')

    if not api_key:
        return jsonify({'message': 'Not logged in 1'}), 401
    response = get_user(api_key)

    if not response.get('result'):
        return jsonify({'message': 'Not logged in 2'}), 401

    client.contact_name = request.json['contact_name']
    client.contact_email = request.json['contact_email']
    client.contact_number = request.json['contact_number']
    db.session.commit()
    return client.serialize()
