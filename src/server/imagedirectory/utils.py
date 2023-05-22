"""
This module provides a set of functions and utilities.
"""
import os
import uuid
from minio import Minio
import re
import json
from flask import request
from werkzeug.exceptions import NotFound, Forbidden
from werkzeug.security import generate_password_hash
from werkzeug.routing import BaseConverter
import secrets

from imagedirectory import constants
from imagedirectory import models

ALLOWED_EXTENSIONS = {'jpg', 'png'}

def require_key(func):
    """
    A decorator function that checks if an API key is present in the request header and if it is valid. 

    Args:
    - func: the function to be decorated

    Returns:
    - wrapper function that either calls the decorated function if the API key is valid, or raises a Forbidden error if it is not.
    """
    def wrapper(*args, **kwargs):
        """
        Inner function that checks if an API key is present in the request header and if it is valid.

        Raises:
        - Forbidden: If the API key is missing or invalid.

        Returns:
        - The decorated function if the API key is valid.
        """
        if request.headers.get("Api-Key") is None:
            raise Forbidden
        key_hash = models.ApiKey.key_hash(request.headers.get("Api-Key").strip()).hex()
        print(key_hash)
        db_key = models.ApiKey.objects(key=key_hash).first()
        if db_key is None:
            raise Forbidden
        print(db_key.key)
        if secrets.compare_digest(key_hash, db_key.key):
            return func(*args, **kwargs)
        raise Forbidden
    return wrapper

class ImageConverter(BaseConverter):
    """
    Flask converter to retrieve an Image object from a URL parameter.

    Args:
        BaseConverter (flask.app.BaseConverter): Base class for Flask URL parameter converters.

    Returns:
        `models.Image`: Image object retrieved from the given URL parameter.

    Raises:
        NotFound: If no Image object is found with the given ID.
    """
    def to_python(self, id):
        """
        Converts the given URL parameter into an Image object.

        Args:
            id (str): URL parameter representing the ID of the Image object to retrieve.

        Returns:
            `models.Image`: Image object retrieved from the given URL parameter.

        Raises:
            NotFound: If no Image object is found with the given ID.
        """
        try:
            db_model = models.Image.objects.get(id=id)
            if db_model is None:
                raise NotFound
            print(db_model.description)
            return db_model
        except Exception as e:
            raise NotFound

    def to_url(self, db_model):
        """
        Converts an Image object into a URL parameter.

        Args:
            db_model (`models.Image`): Image object to convert.

        Returns:
            str: URL parameter representing the ID of the given Image object.
        """
        return db_model.id

class UserConverter(BaseConverter):
    """
    Flask converter to retrieve a User object from a URL parameter.

    Args:
        BaseConverter (flask.app.BaseConverter): Base class for Flask URL parameter converters.

    Returns:
        `models.User`: User object retrieved from the given URL parameter.

    Raises:
        NotFound: If no User object is found with the given username.
    """
    def to_python(self, username):
        """
        Converts the given URL parameter into a User object.

        Args:
            username (str): URL parameter representing the username of the User object to retrieve.

        Returns:
            `models.User`: User object retrieved from the given URL parameter.

        Raises:
            NotFound: If no User object is found with the given username.
        """
        try:
            db_model = models.User.objects(username=username).first()
            if db_model is None:
                raise NotFound
            return db_model
        except Exception as e:
            raise NotFound

    def to_url(self, db_model):
        """
        Converts a User object into a URL parameter.

        Args:
            db_model (`models.User`): User object to convert.

        Returns:
            str: URL parameter representing the username of the given User object.
        """
        return db_model.username

def allowed_file(filename):
    """
    Returns True if the given filename has an allowed extension, else False.

    Args:
        filename (str): The filename to check for allowed extension.

    Returns:
        bool: True if the file extension is allowed, else False.
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_guid():
    """
    Generates a new GUID (globally unique identifier) and returns it as a string.

    Returns:
        str: A string representing the generated GUID.
    """
    guid = str(uuid.uuid4())
    return guid

def get_file_extension(filename):
    """
    Returns the extension of the given filename.

    Args:
        filename (str): The filename to extract extension from.

    Returns:
        str: The extension of the given filename.
    """
    return os.path.splitext(filename)[1]

def validate_username(username):
    """
    Returns True if the given username is valid according to the USERNAME_REGEX pattern,
    else False.

    Args:
        username (str): The username to validate.

    Returns:
        bool: True if the given username is valid, else False.
    """
    pattern = constants.USERNAME_REGEX
    if re.match(pattern, username):
        return True
    return False

def check_username_exist(username):
    """
    Returns True if a user with the given username exists in the database, else False.

    Args:
        username (str): The username to check for existence in the database.

    Returns:
        bool: True if a user with the given username exists in the database, else False.
    """
    user = models.User.objects(username=username).first()
    if user is None:
        return False
    return True

def get_password_hash(password):
    """
    Generates a password hash for the given password and returns it as a string.

    Args:
        password (str): The password to generate hash for.

    Returns:
        str: The generated password hash.
    """
    hashed_password = generate_password_hash(password=password)
    return hashed_password

minio_client = Minio(
    "86.50.229.208:9000",
    access_key="64aHv2etWwD2Y1M4",
    secret_key="bE2gqJKNSwLOITjCfckJPVRySpiUkluv",
    secure=False
)

class ResponseModel:
    """A model representing the response of an API request.

    Attributes:
        data (object): The data returned by the API.
        message (str): A message describing the result of the request.
        error (str): An error message, if any.

    Methods:
        toJSON(): Returns the JSON representation of the model.

    """
    data: object = None
    message: str = None
    error: str = None
    def __init__(self, message = None, data = None, error = None):
        """Initializes a ResponseModel instance.

        Args:
            message (str, optional): A message describing the result of the request.
            data (object, optional): The data returned by the API.
            error (str, optional): An error message, if any.

        """
        self.message = message
        self.data = data
        self.error = error

    def toJSON(self):
        """Returns the JSON representation of the ResponseModel instance.

        Returns:
            str: A string containing the JSON representation of the model.
        """
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

def wrap_response(message = None, data = None):
    """
    Wraps the response data in a ResponseModel object and returns the JSON string representation.

    Args:
        message : str, optional
            A message to be returned in the response. Defaults to None.
        data : object, optional
            The data object to be returned in the response. Defaults to None.

    Returns:
    str
        The JSON string representation of the ResponseModel object containing the message and data.
    """
    res = ResponseModel(message = message, data = data)
    return res.toJSON()

def wrap_error(error):
    """
    Wraps the error message in a ResponseModel object and returns the JSON string representation.

    Parameters:
    -----------
    error : str
        The error message to be returned in the response.

    Returns:
    --------
    str
        The JSON string representation of the ResponseModel object containing the error message.
    """
    res = ResponseModel(error = error)
    return res.toJSON()
