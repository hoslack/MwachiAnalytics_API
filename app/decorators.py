from functools import wraps
from flask import request, jsonify
import jwt
from config import Config
from app.models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message':'Token is missing'}), 401

        try:
            data = jwt.decode(token, Config.SECRET_KEY)
            current_user = User.query.filter_by(data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorated
