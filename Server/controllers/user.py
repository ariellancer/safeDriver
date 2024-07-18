# from Server.models.user import UserModel
from Server.service.user import add_user_service, find_user_service
from flask import request, jsonify
from pydantic import ValidationError
# from Server.controllers.token_controller import decode_token


async def add_user_controller():
    try:
        # Parse the JSON data from the request
        user_data = await request.get_json()

        # Validate the data using Pydantic
        # validated_data = UserModel(**user_data)

        # Create and save the user to MongoDB using the service
        result = await add_user_service(
            firstname=user_data.firstname,
            lastname=user_data.lastname,
            username=user_data.username,
            password=user_data.password
        )

        if result == -1:
            return jsonify({'message': 'User already exists'}), 400

        return jsonify({'message': 'User registered successfully'}), 201

    except ValidationError as e:
        # Return a JSON response with validation errors
        return jsonify({'errors': e.errors()}), 400

    except Exception as e:
        # Handle other exceptions
        return jsonify({'error': str(e)}), 500

# async def find_user_controller(req):
#     token = req.headers.get('Authorization').split(" ")[1]
#     username = decode_token(token)
#     if username == -1:
#         return 401, None
#
#     response = await find_user_service(req.params['username'])
#     if response == -1:
#         return 401, None
#     else:
#         return 200, response
