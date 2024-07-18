from flask import request, jsonify

from Server.service.token import generate_token
from Server.service.user import find_user_service
import hashlib


async def token_controller():
    data = request.get_json()
    username = data['username']
    password = data['password']
    salt_password = username + password
    hash_password = hashlib.sha256(salt_password.encode('utf-8')).hexdigest()
    result = await find_user_service(username, hash_password)
    if result == -1:
        return jsonify(message="Incorrect username and/or password"), 404
    token = generate_token(username, 'admin')
    return jsonify(token=token), 200
