from flask import Flask, request, Response
import pprint
from flask_restful import Api, Resource
from . import models
from mongoengine import *
from minio import Minio
from werkzeug.utils import secure_filename
import uuid
import os
from werkzeug.routing import BaseConverter
from werkzeug.exceptions import NotFound
import datetime
import json
from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

minio_client = Minio(
    "86.50.229.208:9000",
    access_key="8UQvmZYlLMmbdGw4",
    secret_key="VxI9Ig0huEvN07seO168TY6E3eRDZUge",
    secure=False
)

ALLOWED_EXTENSIONS = {'jpg', 'png'}
TEST_USER_ID = "64099805f162b6c56e7ada81"

class UserCollection(Resource):
    def get(self):
        users = models.User.objects
        print(users.to_json())
        return Response(users.to_json(), 200, headers=dict(request.headers))

    def post(self):
        if not request.json:
            Response(status=415)
        user = models.User(email = request.json["email"],
                    first_name = request.json["first_name"],
                    last_name = request.json["last_name"],
                    password_hash = request.json["password_hash"]
                    )
        try:
            user.save()
        except Exception as e:
            return Response(str(e), 400)
        return Response(user.to_json(), 201, headers=dict(request.headers))
    
class ImageCollection(Resource):
    def get(self):
        return Response(models.Image.objects.to_json(), status=200, headers=dict([("Content-Type","application/json")]))
    
    # https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
    def post(self):
        print("Here")
        if 'file' not in request.files:
            return Response("No file attached", 400, headers=dict(request.headers))
        print("Here")
        file = request.files['file']
        filename = secure_filename(file.filename)
        if filename == '':
            return Response("No file attached", 400, headers=dict(request.headers))
        print(file.filename)
        if not file:
            return Response("No file attached", 400, headers=dict(request.headers))
        if not allowed_file(filename):
            return Response("Format unaccepted", 400, headers=dict(request.headers))

        found = minio_client.bucket_exists("images")
        if not found:
            minio_client.make_bucket("images")
        else:
            print("Bucket 'images' already exists")
        file_size = len(file.stream.read())
        file.seek(0)
        generated_guid = generate_guid()
        minio_result = minio_client.put_object(
            "images", f'{generated_guid}{get_file_extension(filename)}', file.stream, file_size
        )
        print(
            "created {0} object; etag: {1}, version-id: {2}".format(
                minio_result.object_name, minio_result.etag, minio_result.version_id,
            ),
        )

        tags_string = request.form.get('tags')
        tags_list = tags_string.replace(' ', '').split(',')
        image = models.Image()
        image.description = request.form.get('description')
        image.tags = tags_list
        image.file_content = models.FileContent(file_name=filename, storage_id=f'{generated_guid}{get_file_extension(filename)}')
        try:
            image.save()
        except Exception as e:
            return Response(str(e), 400)

        return Response(status=201)

class ImageItem(Resource):
    def get(self, image):
        return Response(image.to_json(), status=200, headers=dict(request.headers))
    
    def delete(self, image):
        minio_client.remove_object("images", image.file_content.storage_id)
        image.delete()
        return Response(status=200, headers=dict(request.headers))
    def put(self, image):
        if not request.json:
            Response(status=415)
        description = request.json["description"]
        tags_string = request.json["tags"]

        image.description = description
        image.tags = tags_string.replace(' ', '').split(',')
        image.save()
        return Response(status=200)

class ImageCommentCollection(Resource):
    def post(self, image):
        if not request.json:
            Response(status=415)
        text = request.json["text"]
        user = models.User.objects.get(id=TEST_USER_ID) # TODO: Should be changed with Authenticated user id
        comment = models.Comment(userId=user.id, text=text)
        image.comments.append(comment)
        image.save()
        return Response(status=201)
    
class ImageCommentItem(Resource):
    def delete(self, image, comment_id):
        previous_comment = None
        for comment in image.comments:
            print(type(comment.id))
            print(str(comment.id))
            if str(comment.id) == comment_id:
                previous_comment = comment
        if previous_comment is None:
            return Response("No record exists", status=400)
        image.update(pull__comments=previous_comment)
        return Response(status=200)
    
class ImageLikeCollection(Resource):
    def post(self, image):
        user = models.User.objects.get(id=TEST_USER_ID) # TODO: Should be changed with Authenticated user id
        like = models.Like(userId=user.id, created=datetime.datetime.now())
        image.likes.append(like)
        image.save()
        return Response(status=201)
    
    def delete(self, image):
        user = models.User.objects.get(id=TEST_USER_ID) # TODO: Should be changed with Authenticated user id
        previous_like = None
        for like in image.likes:
            if like.userId.id == user.id:
                previous_like = like
        if previous_like is None:
            return Response("No record exists", status=400)
        image.update(pull__likes=previous_like)
        return Response(status=200)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_guid():
    guid = str(uuid.uuid4())
    return guid

def get_file_extension(filename):
    return os.path.splitext(filename)[1]

# app.url_map.converters["image"] = ImageConverter

api.add_resource(UserCollection, "/users/")
api.add_resource(ImageCollection, "/images/")
api.add_resource(ImageItem, "/images/<image:image>")
api.add_resource(ImageCommentCollection, "/images/<image:image>/comments/")
api.add_resource(ImageCommentItem, "/images/<image:image>/comments/<comment_id>")
api.add_resource(ImageLikeCollection, "/images/<image:image>/likes/")