
from mongoengine import Document, StringField, ListField, IntField


# Connect to MongoDB (replace with your own connection string)

# MongoEngine Schema
class User(Document):
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    username = StringField(required=True)
    password = StringField(required=True)
    statistics = ListField(IntField(), default=lambda: [0] * 12)


