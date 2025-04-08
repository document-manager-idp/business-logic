from functools import wraps
from flask import request, jsonify, g
from app.auth_client import get_userinfo
import app.logger as logger  # Replace with your actual custom logging library

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
