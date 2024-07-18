from flask import Blueprint

from Server.controllers.statistics import get_statistics, update_statistics

get_statistics_bp = Blueprint('get_statistics_bp', __name__)
get_statistics_bp.route('/Statistics', methods=['GET'])(get_statistics)

put_statistics_bp = Blueprint('put_statistics_bp', __name__)
put_statistics_bp.route('/Statistics', methods=['Put'])(update_statistics)
