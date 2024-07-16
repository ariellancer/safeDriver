from typing import Optional

from mongoengine import Document, StringField, EmbeddedDocumentField, ListField
from pydantic import BaseModel, Field, conlist

from Server.models.statistics import Hours, HourSlotModel


# Connect to MongoDB (replace with your own connection string)


# MongoEngine Schema
class User(Document):
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    username = StringField(required=True)
    password = StringField(required=True)
    statistics = ListField(EmbeddedDocumentField(Hours), default=lambda: [Hours() for _ in range(12)])


# Pydantic Model
class UserModel(BaseModel):
    firstname: str = Field(..., title="First Name", description="The first name of the user")
    lastname: str = Field(..., title="Last Name", description="The last name of the user")
    username: str = Field(..., title="Username", description="The username of the user")
    password: str = Field(..., title="Password", description="The password of the user")
    hour_slots: Optional[conlist(HourSlotModel, min_items=12, max_items=12)] = Field(
        default_factory=lambda: [HourSlotModel() for _ in range(12)], title="Hour Slots",
        description="A list of 12 hour slots with percentages")

# def create_user(userdata: dict):
#     # Validate data using Pydantic
#     user_data = UserModel(**userdata)
#
#     # Create and save user to MongoDB
#     user = User(
#         firstname=user_data.firstname,
#         lastname=user_data.lastname,
#         username=user_data.username,
#         password=user_data.password,
#
#     )
#     user.save()
#     # return user
