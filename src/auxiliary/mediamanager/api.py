from flask import Blueprint
from flask_restful import Api
from mediamanager.resources.media import MediaCollection, MediaItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(MediaCollection, "/media/")
api.add_resource(MediaItem, "/media/<storage_id>")
