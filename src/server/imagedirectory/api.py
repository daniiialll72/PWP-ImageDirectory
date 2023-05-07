"""
This module provides resource mappings and blueprints of the application.
"""
from flask_restful import Api
from flask import Blueprint
from imagedirectory.resources.image import ImageCollection, ImageItem
from imagedirectory.resources.user import UserCollection, UserItem
from imagedirectory.resources.imagecomment import ImageCommentCollection, ImageCommentItem
from imagedirectory.resources.imagelike import ImageLikeCollection
from imagedirectory.resources.imagereport import ReportedImageCollection

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(UserCollection, "/users/")
api.add_resource(UserItem, "/users/<user:user>")
api.add_resource(ImageCollection, "/images/")
api.add_resource(ImageItem, "/images/<image:image>")
api.add_resource(ReportedImageCollection, "/images/<image:image>/report")
api.add_resource(ImageCommentCollection, "/images/<image:image>/comments/")
api.add_resource(ImageCommentItem, "/images/<image:image>/comments/<comment_id>")
api.add_resource(ImageLikeCollection, "/images/<image:image>/likes/")