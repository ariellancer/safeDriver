
from jwt import InvalidTokenError
from jwt.exceptions import ExpiredSignatureError
import jwt
import datetime


def generate_token(username, role):
    payload = {
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    try:
        with open('secretKey.txt', 'r') as file:
            secretkey = file.read()
    except FileNotFoundError:
        print("Error: The file was not found.")
        return None
    except IOError:
        print("Error: An I/O error occurred.")
        return None
    token = jwt.encode(payload, secretkey, algorithm='HS256')
    return token


def decode(token: str):
    try:
        try:
            with open('secretKey.txt', 'r') as file:
                secretkey = file.read()
        except FileNotFoundError:
            print("Error: The file was not found.")
            return None
        except IOError:
            print("Error: An I/O error occurred.")
            return None
        decoded_token = jwt.decode(token, secretkey, algorithms=['HS256'])
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


