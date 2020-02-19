from flask import Blueprint, request, jsonify, url_for, redirect
from flask_login import logout_user, login_required
from werkzeug.security import generate_password_hash
from jsonschema import validate, ValidationError
from service.schema import User, LOGIN_ROLE, REGISTER_ROLE

import service.auth_service as service

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET'])
def register_get():
    return "register page"


@auth.route('/register', methods=['POST'])
def register_post():
    try:
        validate(instance=request.json, schema=User.get_schema(role=REGISTER_ROLE))
    except ValidationError:
        return jsonify({'result': 'validation error'})

    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    name = request.json.get('name')

    exist = service.user_already_exists(username=username, email=email)

    if exist:
        return redirect(url_for('auth.register_get'))

    service.new_user(username=username, email=email, name=name,
                     password=generate_password_hash(password, method='sha256'))

    return jsonify({'result': True})


@auth.route('/login', methods=['GET'])
def login_get():
    return "login page"


@auth.route('/login', methods=['POST'])
def login_post():
    try:
        validate(instance=request.json, schema=User.get_schema(role=LOGIN_ROLE))
    except ValidationError:
        return jsonify({'result': 'validation error'})

    username = request.json.get('username')
    password = request.json.get('password')

    flag = service.log_user_in(username, password)
    if flag:
        return "user profile"
    else:
        return redirect(url_for('auth.login_get'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))
