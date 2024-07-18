from flask import Blueprint
from Server.controllers.token import token_controller

login_bp = Blueprint('login_bp', __name__)
login_bp.route('/Login', methods=['POST'])(token_controller)

