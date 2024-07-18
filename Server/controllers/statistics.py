from flask import request, jsonify

from Server.service.statistics import update_statistics_service, get_statistics_service
from Server.service.token import decode, token_required


def get_statistics():
    try:
        headers = dict(request.headers)
        print(headers)
        auth_header = request.headers.get('authorization')
        print(auth_header)
        if not auth_header:
            return jsonify({"error": "Authorization header is missing"}), 401
        # Extract the token from the Authorization header
        token = auth_header.split(" ")[1]
        print(token)

        # Decode the token and get the username
        user = decode(token)
        print(user)
        if not user:
            return jsonify({"error": "Invalid token"}), 401

            # Use the username to fetch Statistics or other information
            # For demonstration, we'll return a dummy response
            # Use the username to fetch Statistics or other information
            statistics = get_statistics_service(user)

            # Create a response object as per client's expectation
            response = {
                "img": statistics  # Assuming `Statistics` is what client expects as `statisticsPic`
            }

            return jsonify(response), 200

    except IndexError:
        return jsonify({"error": "Token not found in Authorization header"}), 401


@token_required
def update_statistics(user):
    try:
        # Extract data from the request body
        data = request.get_json()
        start = data.get('start')
        end = data.get('end')
        unfocused = data.get('unfocused')

        success, message = update_statistics_service(user, start, end, unfocused)
        if success:
            return jsonify({
                'message': 'Statistics updated successfully'}), 200
        else:
            return jsonify({'error': message}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
