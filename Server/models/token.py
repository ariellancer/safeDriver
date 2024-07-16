from mongoengine import Document, StringField


# Define UserPass schema
class UserPass(Document):
    username = StringField(required=True)
    password = StringField(required=True)


# Define Token schema
class Token(Document):
    username = StringField()
    token = StringField()


# Create model for 'androidTokens'
tokenForAndroid = Token.objects

# Export schemas and model
__all__ = ['UserPass', 'tokenForAndroid']
