from app import app
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from app.models import User


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

