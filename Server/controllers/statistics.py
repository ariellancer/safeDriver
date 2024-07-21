from flask import request, jsonify

from Server.service.statistics import update_statistics_service, get_statistics_service
from Server.service.token import decode
from Server.service.user import find_user_by_username_service


async def get_statistics():
    try:
        auth_header = request.headers.get('authorization')
        token = auth_header[19:-8]
        user = decode(token)
        if not user:
            return jsonify({"error": "Authorization header is missing"}), 401
        user = await find_user_by_username_service(user)
        if not user:
            return jsonify({"error": "Invalid token"}), 401
        statistics = get_statistics_service(user)
        # Create a response object as per client's expectation
        response = {
            "img": statistics  # Assuming `Statistics` is what client expects as `statisticsPic`
        }

        return jsonify(response), 200

    except IndexError:
        return jsonify({"error": "Token not found in Authorization header"}), 401


async def update_statistics():
    try:
        auth_header = request.headers.get('authorization')
        token = auth_header[19:-8]
        username = decode(token)
        if not token:
            return jsonify({"error": "Authorization header is missing"}), 401
        data = request.get_json()
        start = data['start']
        end = data['end']
        unfocused = data['unfocused']
        hours_per_cell = 2
        unfocused_array = [0 for i in range(12)]
        total_hours = (end - start) % 24 + 1
        unfocused_per_interval = unfocused // total_hours
        remainder = unfocused % total_hours
        start_index = start
        unfocused_array[start_index // hours_per_cell] += remainder
        for i in range(total_hours):
            unfocused_array[start_index // hours_per_cell] += unfocused_per_interval
            start_index = (start_index + 1) % 24
        success, message = await update_statistics_service(username, unfocused_array)
        if success:
            return jsonify({
                'message': 'Statistics updated successfully'}), 200
        else:
            return jsonify({'error': message}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
