from app import app
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
from datetime import datetime, timedelta
from app.models import User, Order
from config import Config
import logging
from app.decorators import token_required


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


@app.route('/user', methods=['GET'])
def get_current_user():
    token = None
    """Method for getting the current user"""
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']

    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    try:
        data = jwt.decode(token, Config.SECRET_KEY)
        current_user = data['public_id']
    except Exception as e:
        logging.exception(e)
        return jsonify({'message': 'Token is invalid'})

    return jsonify({'current_user': current_user})


@app.route('/order', methods=['POST'])
def create_order():
    data = request.get_json()
    public_id = str(uuid.uuid4())
    phone_number = data['phone_number']
    how_to_contact = data['how_to_contact']
    leading_channel = data['leading_channel']
    project_type = data['project_type']
    software_requirements = data['software_requirements']
    description = data['description']
    created_by = data['created_by']
    order = Order(public_id=public_id, phone_number=phone_number, how_to_contact=how_to_contact,
                  leading_channel=leading_channel, project_type=project_type,
                  software_requirements=software_requirements, description=description, created_by=created_by)

    order.save()
    return jsonify({'message': 'order created successfully'})


@app.route('/order', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    if not orders:
        return jsonify({'message': 'There are no orders found'})
    output = []
    for order in orders:
        order_data = {}
        order_data['public_id'] = order.public_id
        order_data['description'] = order.description
        output.append(order_data)

    return jsonify({'orders': output})


@app.route('/order/<public_id>', methods=['DELETE'])
def delete_order(public_id):
    order = Order.query.filter_by(public_id=public_id).first()
    if not order:
        return jsonify({'message': 'The order does not exist'})
    order.delete()
    return jsonify({'message': 'The order was deleted successfully'})


@app.route('/order/<public_id>', methods=['PUT'])
def update_order(public_id):
    data = request.get_json()
    order = Order.query.filter_by(public_id=public_id)
    order.paid = data['paid']
    order.save()
    return jsonify({'message': 'The order was updated successfully'})











