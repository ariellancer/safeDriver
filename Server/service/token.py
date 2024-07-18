from functools import wraps

from flask import request, jsonify
from jwt import ExpiredSignatureError, InvalidTokenError

from Server.models.user import User
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
        # Decode the token and verify its signature
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        # Access the username from the decoded token
        username = decoded_token.get('username')
        user = User.objects(username=username).first()
        # Perform any additional validation if necessary
        if user:
            return user
        else:
            print("Username not found in token")
            return None

    except ExpiredSignatureError:
        print("Token has expired")
        return None

    except InvalidTokenError:
        print("Invalid token")
        return None

    except KeyError:
        print("Username not found in token")
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            user = decode(token)
            if user is None:
                return jsonify({'message': 'Token is invalid!'}), 401
        except Exception as e:
            return jsonify({'message': str(e)}), 500

        return f(user, *args, **kwargs)

    return decorated
