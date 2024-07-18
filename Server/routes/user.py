from fastapi import APIRouter, HTTPException, Request
from flask import Blueprint
from Server.controllers.user import add_user_controller

# router = APIRouter()

register_bp = Blueprint('register_bp', __name__)
register_bp.route('/Register', methods=['POST'])(add_user_controller)




# @router.post("/")
# async def add_user_route(req: Request):
#     status_code, response = await add_user_controller(req)
#     if status_code == 200:
#         return {}
#     else:
#         raise HTTPException(status_code=status_code)


# @router.get("/{username}")
# async def find_user_route(req: Request, username: str):
#     status_code, response = await find_user_controller(req)
#     if status_code == 200:
#         return response
#     else:
#         raise HTTPException(status_code=status_code)
