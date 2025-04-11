from functools import wraps
from flask import request, jsonify, g
from app.auth_client import get_userinfo
import sys
if '..' not in sys.path: sys.path.append('..')
from utils import get_logger

logger = get_logger(__name__)

def auth_route(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Log the incoming request details for debugging purposes
        logger.info("Incoming request %s %s", request.method, request.url)

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            logger.warning("Missing Authorization header in the request")
            return jsonify({"error": "Missing Authorization header"}), 400

        if not auth_header.startswith('Bearer '):
            logger.warning("Invalid Authorization header format: %s", auth_header)
            return jsonify({"error": "Invalid Authorization header format"}), 400

        token = auth_header.split(' ')[1]
        logger.debug("Extracted token: %s", token)

        user_credentials = get_userinfo(token)
        if not user_credentials:
            logger.error("Failed to retrieve user credentials for token: %s", token)
            return jsonify({"error": "Failed to retrieve user credentials"}), 403

        # Store user credentials in Flask's global object for later use in the route
        g.user = user_credentials
        logger.info("User authenticated: %s", user_credentials.get("username", "unknown"))
        return f(*args, **kwargs)
    return decorated_function

def require_request_params(*parameters):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No JSON payload provided'}), 400

            missing_params = [param for param in parameters if not data.get(param)]
            if missing_params:
                return jsonify({'error': f'Missing required field(s): {missing_params}'}), 400

            return f(*args, **kwargs)
        return decorated_function
    return wrapper
