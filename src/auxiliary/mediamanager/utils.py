"""
This module provides a set of functions and utilities.
"""
import os
import uuid
from minio import Minio
import json

ALLOWED_EXTENSIONS = {'jpg', 'png'}

def allowed_file(filename):
    """
    Check if a filename is allowed based on its extension.

    Parameters
    ----------
    filename : str
        The name of the file to check.

    Returns
    -------
    bool
        True if the file is allowed, False otherwise.
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_guid():
    """
    Generate a unique identifier (GUID) using the UUID library.

    Returns
    -------
    str
        A string representing the generated GUID.
    """
    guid = str(uuid.uuid4())
    return guid

def get_file_extension(filename):
    """
    Get the extension of a file from its filename.

    Parameters
    ----------
    filename : str
        The name of the file.

    Returns
    -------
    str
        The extension of the file, including the dot (e.g., ".txt").
    """
    return os.path.splitext(filename)[1]

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
