from mongoengine import *

class User(Document):
    email = EmailField(required=True)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    password_hash = StringField(required=True, max_length=50)
    gender = StringField( choices=['male', 'female', 'others'])

class Like(EmbeddedDocument):
    userId = ReferenceField(User)
    createdAt = DateTimeField(required=True)

class Comment(EmbeddedDocument):
    userId = ReferenceField(User)
    text = StringField(required=True)

class FileContent(EmbeddedDocument):
    file_name = StringField(required=True)
    storage_id = StringField(required=True)

class Image(Document):
    userId = ReferenceField(User)
    description = StringField(max_length=150)
    tags = ListField(StringField())
    file_content = EmbeddedDocumentField(FileContent)
    likes = ListField(EmbeddedDocumentField(Like))
    comments = ListField(EmbeddedDocumentField(Comment))
    # createdAt = DateTimeField(required=True)
    # updatedAt = DateTimeField()
    # isAbused = BooleanField(required=True, default=False)

class Admin(Document):
    username = StringField(required=True)
    email = StringField(required=True)
    password = StringField(required=True)
    phone = StringField()
    createdAt = DateTimeField(required=True)
    updatedAt = DateTimeField(required=True)