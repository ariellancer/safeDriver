from flask import Blueprint

from Server.controllers.model import process_model_request

model_bp = Blueprint('model_bp', __name__)
model_bp.route('/Model', methods=['GET'])(process_model_request)
