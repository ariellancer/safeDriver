from mongoengine import DoesNotExist
from Server.models.user import User


async def add_user_service(firstname: str, lastname: str, username: str, password: str):
    # Check if the user already exists
    try:
        existing_user = User.objects.get(username=username)
        return -1  # User already exists
    except DoesNotExist:

        new_user = User(
            username=username,
            password=password,
            firstname=firstname,
            lastname=lastname
        )
        # Create a new user
        # new_user = User(
        #     username=user_data.username,
        #     password=user_data.password,
        #     firstname=user_data.firstname,
        #     lastname=user_data.lastname
        # )
        new_user.save()
        return 1  # User added successfully


async def find_user_service(username: str, password: str):
    user = User.objects(username=username, password=password).first()
    if user:
        return 1
    else:
        return -1


async def find_user_by_username_service(username: str):
    try:
        user = User.objects(username=username).first()
        if user:
            return user
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
