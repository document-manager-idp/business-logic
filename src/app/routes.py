from flask import Blueprint, request, jsonify, g
from app.decorators import auth_route

main_bp = Blueprint('main', __name__)

@main_bp.route('/profile', methods=['GET'])
@auth_route
def profile():
    # The user's credentials are now available in g.user
    return jsonify({"user": g.user}), 200

@main_bp.route('/upload', methods=['POST'])
@auth_route
def upload():
     # Another endpoint using the same authentication logic
    username = g.user.get('username', 'User')
    return jsonify({"message": f"Hello, {username}!"}), 200
