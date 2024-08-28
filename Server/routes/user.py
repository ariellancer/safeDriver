
from flask import Blueprint
from Server.controllers.user import add_user_controller


# router = APIRouter()
register_bp = Blueprint('register_bp', __name__)
register_bp.route('/Register', methods=['post'])(add_user_controller)




