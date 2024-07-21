from Server.service.user import add_user_service
from flask import request, jsonify
from pydantic import ValidationError
import hashlib


async def add_user_controller():
    try:
        user_data = request.get_json()
        firstname = user_data["firstname"]
        lastname = user_data["lastname"]
        username = user_data["username"]
        salt_password = username + user_data["password"]
        hash_password = hashlib.sha256(salt_password.encode('utf-8')).hexdigest()
        result = await add_user_service(
            firstname=firstname,
            lastname=lastname,
            username=username,
            password=hash_password
        )

        if result == -1:
            return jsonify({'message': 'User already exists'}), 403

        return jsonify({'message': 'User registered successfully'}), 200

    except ValidationError as e:
        return jsonify({'errors': e.errors()}), 400

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
