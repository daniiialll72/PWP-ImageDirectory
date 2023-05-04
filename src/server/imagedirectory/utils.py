from werkzeug.routing import BaseConverter
from werkzeug.exceptions import Forbidden, NotFound
import os
import uuid
from minio import Minio
import re
from werkzeug.security import generate_password_hash
from imagedirectory.constants import USERNAME_REGEX
from imagedirectory import models
import json

ALLOWED_EXTENSIONS = {'jpg', 'png'}

class ImageConverter(BaseConverter):
    def to_python(self, id):
        print("*******")
        db_model = models.Image.objects.get(id=id)
        if db_model is None:
            raise NotFound #TODO: Which one is best practice
        print("&&&&&&&&&&&")
        print(db_model.description)
        return db_model
        
    def to_url(self, db_model):
        return db_model.id
    
class UserConverter(BaseConverter):
    def to_python(self, username):
        db_model = models.User.objects(username=username).first()
        if db_model is None:
            raise NotFound #TODO: Which one is best practice
        return db_model
        
    def to_url(self, db_model):
        return db_model.username

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_guid():
    guid = str(uuid.uuid4())
    return guid

def get_file_extension(filename):
    return os.path.splitext(filename)[1]

def validate_username(username):
    # define the regular expression pattern
    pattern = USERNAME_REGEX
    if re.match(pattern, username):   
        return True
    else:
        return False

def check_username_exist(username):
    user = models.User.objects(username=username).first()
    if user is None:
        return False
    return True
    
def get_password_hash(password):
    hashed_password = generate_password_hash(password=password)
    return hashed_password

minio_client = Minio(
    "86.50.229.208:9000",
    access_key="8UQvmZYlLMmbdGw4",
    secret_key="VxI9Ig0huEvN07seO168TY6E3eRDZUge",
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