from flask import request, jsonify

from Server.service.token import generate_token
from Server.service.user import find_user_service


async def token_controller():
    data = await request.get_json()
    username = data.get('username')
    password = data.get('password')
    result = await find_user_service(username, password)
    if result == -1:
        return jsonify(message="Incorrect username and/or password"), 404
    token = generate_token(username, 'admin')
    return jsonify(token=token), 200
