from flask import request, jsonify

from Server.service.model import decode_and_process_pictures
from Server.service.token import decode
from Server.service.user import find_user_by_username_service


async def process_model_request():
    try:
        # Extract data from the request body (check)
        data = request.get_json()
        pictures_base64 = data['pictures']
        if not pictures_base64:
            return jsonify({'message': 'No pictures provided!'}), 400
        auth_header = request.headers.get('authorization')
        token = auth_header[19:-8]
        user = decode(token)
        if not user:
            return jsonify({"error": "Authorization header is missing"}), 401
        user = await find_user_by_username_service(user)
        check = decode_and_process_pictures(user.username, pictures_base64)
        inverted_result = 1 if check == 0 else 0

        return jsonify({
            'message': 'Check processed successfully',
            'result': inverted_result
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
