from mongoengine import *

class User(Document):
    email = EmailField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    password_hash = StringField(max_length=50)
    gender = StringField( choices=['male', 'female', 'Unknown']) 