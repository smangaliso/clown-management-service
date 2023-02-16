from flask import Blueprint, jsonify, request, make_response
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

user_blueprint = Blueprint('user_api_routes', __name__, url_prefix='/')


@user_blueprint.route('/register', methods=['POST'])
def create_user():
    try:
        user = User()
        user.email = request.json.get('email')
        user.password = generate_password_hash(request.json.get('password'), method='sha256')

        db.session.add(user)
        db.session.commit()

        response = {
            "message": "User Created",
            "result": user.serialize()
        }

    except Exception as e:

        response = {'message': 'Error in creating a response'}, 401

    return jsonify(response)


@user_blueprint.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        response = {"message": "user does not exist"}
        return make_response(jsonify(response), 401)
    if check_password_hash(user.password, password):
        user.update_api_key()
        db.session.commit()
        login_user(user)
        response = {'message': 'logged in ', 'api_key': user.api_key}
        return make_response(jsonify(response), 200)

    response = {'message': 'access denied'}
    return make_response(jsonify(response), 402)


@user_blueprint.route('logout', methods=['POST'])
def logout():
    if current_user.is_active:
        logout_user()

        return jsonify({"message": "logged out"})

    return jsonify({"message": "not logged in"})


@user_blueprint.route('/current-user', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({'result': current_user.serialize()}), 200
    return jsonify({'result': "User not logged in"}), 400
