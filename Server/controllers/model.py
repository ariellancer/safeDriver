from flask import request, jsonify

from Server.service.token import decode


def process_model_request():
    try:
        # Get the Authorization token from the headers
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        # Decode and validate the token
        decoded_token = decode(token)
        if not decoded_token:
            return jsonify({'message': 'Token is invalid!'}), 401

        # Extract data from the request body (check)
        data = request.get_json()
        check = data.get('pictures')

        # Process the check (pictures array)
        # For example, you could save it to the database or perform some computation

        return jsonify({
            'message': 'Check processed successfully',
            'pictures': check
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
