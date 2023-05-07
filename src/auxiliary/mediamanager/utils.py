from werkzeug.routing import BaseConverter
from werkzeug.exceptions import Forbidden, NotFound
import os
import uuid
from minio import Minio
import re
from werkzeug.security import generate_password_hash
import json
from mediamanager.constants import USERNAME_REGEX

ALLOWED_EXTENSIONS = {'jpg', 'png'}

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_guid():
    guid = str(uuid.uuid4())
    return guid

def get_file_extension(filename):
    return os.path.splitext(filename)[1]

minio_client = Minio(
    "86.50.229.208:9000",
    access_key="64aHv2etWwD2Y1M4",
    secret_key="bE2gqJKNSwLOITjCfckJPVRySpiUkluv",
    secure=False
)

class ResponseModel:
    data: object = None
    message: str = None
    error: str = None
    def __init__(self, message = None, data = None, error = None):
        self.message = message
        self.data = data
        self.error = error

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def wrap_response(message = None, data = None):
    res = ResponseModel(message = message, data = data)
    return res.toJSON()


def wrap_error(error):
    res = ResponseModel(error = error)
    return res.toJSON()