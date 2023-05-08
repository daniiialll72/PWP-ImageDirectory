"""
This module provides a set of classes which are used in the application.
"""
import hashlib
from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmailField,
    EmbeddedDocument,
    EmbeddedDocumentField,
    ListField,
    ObjectIdField,
    ReferenceField,
    StringField,
)
from bson.objectid import ObjectId

from imagedirectory.constants import USERNAME_REGEX

class User(Document):
    """
    Represents a user in the system.

    :param username: The unique username of the user. Must match the regex pattern specified by USERNAME_REGEX.
    :type username: str
    :param email: The email address of the user.
    :type email: str
    :param first_name: The first name of the user.
    :type first_name: str
    :param last_name: The last name of the user.
    :type last_name: str
    :param gender: The gender of the user. Must be one of 'male', 'female', or 'others'.
    :type gender: str
    :param password_hash: The hashed password of the user.
    :type password_hash: str
    """
    username = StringField(required=True, unique=True, regex=USERNAME_REGEX)
    email = EmailField(required=True, unique=True)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    gender = StringField( choices=['male', 'female', 'others'])
    password_hash = StringField(required=True, max_length=250)

class Like(EmbeddedDocument):
    """
    Embedded document representing a like made by a user on an item.

    Attributes:
    - user_id: ReferenceField to the User who made the like.
    - created: DateTimeField representing the date and time when the like was created.
    """
    user_id = ReferenceField(User)
    created = DateTimeField(required=True)

class Comment(EmbeddedDocument):
    """
    A class representing a comment made on an image.

    Attributes
    ----------
    id : bson.ObjectId
        The unique identifier for the comment.
    user_id : User
        The user who made the comment.
    text : str
        The comment text.
    """
    id = ObjectIdField(required=True, 
                        default=ObjectId, 
                        primary_key=True)
    user_id = ReferenceField(User)
    text = StringField(required=True)

class FileContent(EmbeddedDocument):
    """
    A class representing the contents of an image file.

    Attributes
    ----------
    file_name : str
        The name of the image file.
    storage_id : str
        The unique identifier for the image file in storage.
    """
    file_name = StringField(required=True)
    storage_id = StringField(required=True)

class Image(Document):
    """
    A class representing an image.

    Attributes
    ----------
    user_id : User
        The user who uploaded the image.
    description : str
        A description of the image.
    tags : list of str
        A list of tags associated with the image.
    file_content : FileContent
        The contents of the image file.
    likes : list of Like
        A list of likes on the image.
    comments : list of Comment
        A list of comments on the image.
    created_at : datetime.datetime
        The date and time when the image was uploaded.
    updated_at : datetime.datetime
        The date and time when the image was last updated.
    is_abused : bool
        A flag indicating whether the image has been reported as abusive.
    """
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
    """
    A class representing an administrator account.

    Attributes
    ----------
    username : str
        The username of the admin account. Must be unique and match the USERNAME_REGEX pattern.
    email : str
        The email address associated with the admin account.
    password : str
        The password for the admin account.
    created_at : datetime.datetime
        The date and time the admin account was created.
    updated_at : datetime.datetime, optional
        The date and time the admin account was last updated.
    """
    username = StringField(required=True, unique=True, regex=USERNAME_REGEX)
    email = EmailField(required=True)
    password = StringField(required=True)
    created_at = DateTimeField(required=True)
    updated_at = DateTimeField()
    
class ReportedImage(Document):
    """
    A class representing a reported image.

    Attributes
    ----------
    user_id : User
        The user who reported the image.
    image_id : Image
        The image that was reported.
    reason : str
        The reason why the image was reported.
    accepted : bool, optional
        Whether or not the report was accepted by an administrator.
    created_at : datetime.datetime
        The date and time the report was created.
    """
    user_id = ReferenceField(User)
    image_id = ReferenceField(Image)
    reason = StringField(required=True, max_length=150)
    accepted = BooleanField()
    created_at = DateTimeField(required=True)

class ApiKey(Document):
    """
    A class representing a API Keys. From example 
    https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/implementing-rest-apis-with-flask/#api-authentication

    Attributes
    ----------
    key : str
        The key is in an string hashed format.
    """
    key = StringField(required=True, max_length=64, unique=True)

    @staticmethod
    def key_hash(key):
        return hashlib.sha256(key.encode()).digest()