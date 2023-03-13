from mongoengine import *
from bson.objectid import ObjectId
from imagedirectory.constants import USERNAME_REGEX

class User(Document):
    username = StringField(required=True, unique=True, regex=USERNAME_REGEX)
    email = EmailField(required=True, unique=True)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    gender = StringField( choices=['male', 'female', 'others'])
    password_hash = StringField(required=True, max_length=250)

class Like(EmbeddedDocument):
    user_id = ReferenceField(User)
    created = DateTimeField(required=True)

class Comment(EmbeddedDocument):
    id = ObjectIdField(required=True, 
                        default=ObjectId,
                        unique=True, 
                        primary_key=True)
    user_id = ReferenceField(User)
    text = StringField(required=True)

class FileContent(EmbeddedDocument):
    file_name = StringField(required=True)
    storage_id = StringField(required=True)

class Image(Document):
    user_id = ReferenceField(User)
    description = StringField(max_length=150)
    tags = ListField(StringField())
    file_content = EmbeddedDocumentField(FileContent)
    likes = ListField(EmbeddedDocumentField(Like))
    comments = ListField(EmbeddedDocumentField(Comment))
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField()
    is_abused = BooleanField(required=True, default=False)

class Admin(Document):
    username = StringField(required=True, unique=True, regex=USERNAME_REGEX)
    email = EmailField(required=True)
    password = StringField(required=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField()
    
class ReportedImage(Document):
    user_id = ReferenceField(User)
    image_id = ReferenceField(Image)
    reason = StringField(required=True, max_length=150)
    accepted = BooleanField()
    created_at = DateTimeField(required=True)
    