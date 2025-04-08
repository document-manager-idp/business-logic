import requests
import os
from flask import g
import app.logger as logger

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5700')

def build_url(endpoint):
    return f'http://{DB_HOST}:{DB_PORT}/{endpoint}'

def db_search(query):
    url = build_url("db-service/search")

    id = g.user.get('username', 'User')
    body = {
        "id": id,
        "query": query
    }

    response = requests.get(url, json=body)
    logger.info(response.text)
    logger.info(response.status_code)
    if response:
        return response.json()

    return None
