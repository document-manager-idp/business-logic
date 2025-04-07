from functools import wraps
from flask import request, jsonify, g
from app.auth_client import get_userinfo

def auth_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Missing Authorization header"}), 400

        if not auth_header.startswith('Bearer '):
            return jsonify({"error": "Invalid Authorization header format"}), 400

        token = auth_header.split(' ')[1]
        user_credentials = get_userinfo(token)
        if not user_credentials:
            return jsonify({"error": "Failed to retrieve user credentials"}), 403

        # Store user credentials in Flask's global object
        g.user = user_credentials
        return f(*args, **kwargs)
    return decorated_function
