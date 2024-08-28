
from jwt import InvalidTokenError
from jwt.exceptions import ExpiredSignatureError
import jwt
import datetime

SECRET_KEY = 'LOL'


def generate_token(username, role):
    payload = {
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token


def decode(token: str):
    """
    Decode a JWT token, validate it, and extract the username.

    Args:
        token (str): The JWT token to decode.

    Returns:
        str: The username extracted from the token if valid.
        None: If the token is invalid or expired.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username = decoded_token['username']
        return username
    except ExpiredSignatureError:
        print("Token has expired")
        return None

    except InvalidTokenError:
        print("Invalid token")
        return None

    except KeyError:
        print("Username not found in token")
        return None


