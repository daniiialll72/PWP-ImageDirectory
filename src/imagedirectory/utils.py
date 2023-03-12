from werkzeug.routing import BaseConverter
from . import models
from werkzeug.exceptions import Forbidden, NotFound
import os
import uuid
from minio import Minio

ALLOWED_EXTENSIONS = {'jpg', 'png'}

class ImageConverter(BaseConverter):
    def to_python(self, id):
        db_model = models.Image.objects.get(id=id)
        if db_model is None:
            raise NotFound #TODO: Which one is best practice
        return db_model
        
    def to_url(self, db_model):
        return db_model.id

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
    access_key="8UQvmZYlLMmbdGw4",
    secret_key="VxI9Ig0huEvN07seO168TY6E3eRDZUge",
    secure=False
)