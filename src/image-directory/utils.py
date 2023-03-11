from werkzeug.routing import BaseConverter
from . import models
from werkzeug.exceptions import Forbidden, NotFound

class ImageConverter(BaseConverter):
    def to_python(self, id):
        db_model = models.Image.objects.get(id=id)
        if db_model is None:
            raise NotFound #TODO: Which one is best practice
        return db_model
        
    def to_url(self, db_model):
        return db_model.id