from flask import request, jsonify

from Server.service.model import decode_and_process_pictures
from Server.service.token import token_required


@token_required
def process_model_request(user):
    try:
        # Extract data from the request body (check)
        data = request.get_json()
        pictures_base64 = data.get('pictures')

        if not pictures_base64:
            return jsonify({'message': 'No pictures provided!'}), 400

        # Decode and process the pictures using the separate function
        check = decode_and_process_pictures(user.username, pictures_base64)
        inverted_result = 1 if check == 0 else 0

        return jsonify({
            'message': 'Check processed successfully',
            'result': inverted_result
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
