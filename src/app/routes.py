from flask import Blueprint, request, jsonify, g
from app.decorators import auth_route
from app.db_client import *

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

@main_bp.route('/delete', methods=['DELETE'])
@auth_route
def delete():
    username = g.user.get('username', 'User')
    return jsonify({"message": f"Hello, {username}!"}), 200

@main_bp.route('/search', methods=['GET'])
@auth_route
def search():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON payload provided'}), 400
    
    query = data.get("query")
    if not query:
        return jsonify({'error': f'Required field "query" missing'}), 400

    response = db_search(query)

    return jsonify({"content": response}), 200
