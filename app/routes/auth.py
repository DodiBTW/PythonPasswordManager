from flask import request, jsonify, make_response, render_template
from jwt import encode, decode
import datetime
import run
import jwt
from flask import Blueprint
from app.db.user_handler import UserHandler
from flask import redirect, url_for
from app.db.passwords_handler import PasswordsHandler
from app.db.logs_handler import LogsHandler
from cryptography.fernet import Fernet
import bcrypt

user_handler = UserHandler()
logs_handler = LogsHandler()

auth_bp = Blueprint('auth', __name__)

def register():
    if request.method == 'POST':
        data = request.form
        username = data['username']
        password = data['password']
        key = Fernet.generate_key()
        crypted_key = bcrypt.hashpw(key, bcrypt.gensalt())
        if user_handler.user_exists(username):
            return make_response(jsonify({'message': 'User already exists'}), 400)
        encrypted_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user_handler.register(username, encrypted_password, crypted_key)
        return render_template('register.html', key=key.decode())
    return render_template('register.html')
auth_bp = Blueprint('auth', __name__)

def login():
    data = request.form
    username = data['username']
    password = data['password']
    if not user_handler.user_exists(username):
        return make_response(jsonify({'message': 'Invalid credentials'}), 401)
    user_id = user_handler.get_user_id(username)
    encrypted_password = user_handler.get_password(user_id)
    if not user_handler.login(user_id, password):
        return make_response(jsonify({'message': 'Invalid credentials'}), 401)
    key = data['key'].encode()
    crypted_key = user_handler.get_crypted_key(user_id)
    if not bcrypt.checkpw(key, crypted_key):
        return make_response(jsonify({'message': 'Invalid key'}), 401)
    token = encode(
        {
            'user_id': user_id,
            'key': key.decode(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        run.get_secret_key(),
        algorithm='HS256'
    )
    response = make_response(redirect('/home'))
    response.set_cookie('token', token, httponly=True, secure=False)
    response.set_cookie('user_id', str(user_id), httponly=True, secure=False)
    return response
def verify_token(token, user_id):
    if not token:
        return False
    try:
        decoded_token = decode(token, run.get_secret_key(), algorithms=['HS256'])
        user_id_to_check = decoded_token['user_id']
        expiration = datetime.datetime.utcfromtimestamp(decoded_token['exp'])
        if str(user_id_to_check) != str(user_id) or expiration < datetime.datetime.utcnow():
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    return True
def get_key_from_token(token):
    if not token:
        return None
    try :
        decoded_token = decode(token, run.get_secret_key(), algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return None
    except jwt.ExpiredSignatureError:
        return None
    return decoded_token['key'].encode()
@auth_bp.route('/delete_user', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    user_id = data["user_id"]
    token = data['token']
    if not verify_token(token, user_id):
        return make_response(jsonify({'message': 'Invalid token'}), 401)
    user_handler.delete_user(user_id)
    return make_response(jsonify({'message': 'User deleted successfully'}), 200)
@auth_bp.route('/change_password', methods=['PUT'])
def change_password():
    data = request.get_json()
    user_id = data["user_id"]
    password = data['password']
    token = data['token']
    if not verify_token(token):
        return make_response(jsonify({'message': 'Invalid token'}), 401)
    user_handler.change_password(user_id, password)
    return make_response(jsonify({'message': 'Password changed successfully'}), 200)
@auth_bp.route('/logout', methods=['POST'])
def logout():
    token = encode(
        {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1)
        },
        run.get_secret_key(),
        algorithm='HS256'
    )
    response = make_response(jsonify({'message': 'Logged out successfully'}), 200)
    response.set_cookie('token', token, httponly=True, secure=False)
    response.set_cookie('user_id', '', httponly=True, secure=False)
    return response