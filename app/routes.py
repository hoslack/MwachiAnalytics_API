from app import app
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
from datetime import datetime, timedelta
from app.models import User
from config import Config


@app.route('/')
@app.route('/index')
def hello_world():
    return 'Hello World!'


@app.route('/auth/register', methods=['POST'])
def register_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    user = User(public_id=str(uuid.uuid4()), username=data['username'], email=data['email'], password=hashed_password)
    user.save()
    return jsonify({'message': 'User created in the database'})


@app.route('/user/<public_id>', methods=['GET'])
def get_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    output = []
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['username'] = user.username
    user_data['email'] = user.email
    output.append(user_data)
    return jsonify({'data': output})


@app.route('/auth/login', methods=['POST'])
def login():
    secret = Config.SECRET_KEY
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic-realm="Login Required!"'})
    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic-realm="Login Required!"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id, 'exp': datetime.utcnow() + timedelta(minutes=30)}, secret,
                           algorithm='HS256')

        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic-realm="Login Required!"'})







