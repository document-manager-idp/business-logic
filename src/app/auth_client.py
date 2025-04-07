import requests
import os

AUTH_HOST = os.environ.get('AUTH_HOST', 'localhost')
AUTH_PORT = os.environ.get('AUTH_PORT', '3000')

def build_url(endpoint):
    return f'http://{AUTH_HOST}:{AUTH_PORT}/{endpoint}'

def get_userinfo(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    try:
        response = requests.get(build_url("auth/management/userinfo"), headers=headers)
    except requests.exceptions.RequestException:
        return None

    if response.status_code != 200:
        return None

    return response.json()
