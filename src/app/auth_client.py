import requests
import os
import logger

AUTH_HOST = os.environ.get('AUTH_HOST', 'localhost')
AUTH_PORT = os.environ.get('AUTH_PORT', '3000')

def build_url(endpoint):
    return f'http://{AUTH_HOST}:{AUTH_PORT}/{endpoint}'

def get_userinfo(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    url = build_url("auth/management/userinfo")
    logger.info("Sending request to get user info from %s", url)
    try:
        response = requests.get(url, headers=headers)
        logger.debug("Received response with status code: %s", response.status_code)
    except requests.exceptions.RequestException as e:
        logger.error("RequestException occurred while contacting %s: %s", url, e)
        return None

    if response.status_code != 200:
        logger.warning("Request to %s failed with status code: %s", url, response.status_code)
        return None

    user_info = response.json()
    logger.info("Successfully retrieved user info: %s", user_info)
    return user_info
