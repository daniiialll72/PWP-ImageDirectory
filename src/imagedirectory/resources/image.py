from flask import Flask, request, Response
from flask_restful import Api, Resource
from imagedirectory import models
from mongoengine import *
from werkzeug.utils import secure_filename
from imagedirectory import utils
from datetime import datetime
from imagedirectory import cache
from imagedirectory import viewmodels


class ImageCollection(Resource):
    @cache.cached(timeout=300)
    def get(self):
        print("No cached")
        try:
          images = models.Image.objects
          response = Response()
          response.headers['Content-Type'] = "application/json"
          response.status = 200
          response.data = utils.wrap_response(data=viewmodels.convert_images(images))
          return response
        except Exception as e:
          print("Error: ", e)
          return Response(utils.wrap_response(data=str(e)), 500)
    
    # https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
    def post(self):
        print("Here")
        if 'file' not in request.files:
            return Response("No file attached", 400, headers=dict(request.headers)) # Wrong way
        print("Here")
        file = request.files['file']
        filename = secure_filename(file.filename)
        if filename == '':
            return Response("No file attached", 400, headers=dict(request.headers))
        print(file.filename)
        if not file:
            return Response("No file attached", 400, headers=dict(request.headers))
        if not utils.allowed_file(filename):
            return Response("Format unaccepted", 400, headers=dict(request.headers))

        found = utils.minio_client.bucket_exists("images")
        if not found:
            utils.minio_client.make_bucket("images")
        else:
            print("Bucket 'images' already exists")
        file_size = len(file.stream.read())
        file.seek(0)
        generated_guid = utils.generate_guid()
        minio_result = utils.minio_client.put_object(
            "images", f'{generated_guid}{utils.get_file_extension(filename)}', file.stream, file_size
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
        image.created_at = datetime.now()
        image.file_content = models.FileContent(file_name=filename, storage_id=f'{generated_guid}{utils.get_file_extension(filename)}')
        try:
            image.save()
        except Exception as e:
            return Response(str(e), 400)

        return Response(status=201)

class ImageItem(Resource):
    @cache.cached(timeout=300)
    def get(self, image):
        print("No cached")
        return Response(image.to_json(), status=200, headers=dict(request.headers))
    
    def delete(self, image):
        utils.minio_client.remove_object("images", image.file_content.storage_id)
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