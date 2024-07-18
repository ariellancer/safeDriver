from typing import Optional

from mongoengine import Document, StringField, EmbeddedDocumentField, ListField, IntField
from pydantic import BaseModel, Field, conlist


# Connect to MongoDB (replace with your own connection string)

# MongoEngine Schema
class User(Document):
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    username = StringField(required=True)
    password = StringField(required=True)
    statistics = ListField(IntField(), default=lambda: [0] * 12)


# Pydantic Model
# class UserModel(BaseModel):
#     firstname: str = Field(..., title="First Name", description="The first name of the user")
#     lastname: str = Field(..., title="Last Name", description="The last name of the user")
#     username: str = Field(..., title="Username", description="The username of the user")
#     password: str = Field(..., title="Password", description="The password of the user")
#     Statistics: Optional[conlist(int, min_items=12, max_items=12)] = Field(
#         default_factory=lambda: [0] * 12, title="Statistics",
#         description="A list of 12 hour slots with integers"
#     )
