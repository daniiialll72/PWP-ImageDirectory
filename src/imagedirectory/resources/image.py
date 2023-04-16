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
        """
        ---
        description: Get the list of users
        responses:
          '200':
            description: List of users
            content:
              application/json:
                example:
                - email: "evan@gmail.com"
                  first_name: "Mehrdad"
                  gender: "male"
                  last_name: "Kaheh"
                  password_hash: "pbkdf2:sha256:260000$N33Rqt3K6Ha8MTz6$a6c092e00c3da2009649b26d81617e533de24913ebfe3179ac1f4af81e57fd30"
                  username: "Evan"
                - email: "eggege@gmail.com"
                  first_name: "Mehrdad"
                  gender: "male"
                  last_name: "Kaheh"
                  password_hash: "pbkdf2:sha256:260000$bWcuBNkL0UKRTjp6$50d81ea5b010cb9132960530d736739c7e29449a3386cf242e67dbb5f26100cb"
                  username: "efefefef"
        """
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
          return Response(utils.wrap_error(error=str(e)), 500)
    
    # https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
    def post(self):
        """
        ---
        description: Get the list of users
        requestBody:
          content:
            multipart/form-data:
              schema:
                type: object
                properties:
                  file:
                    type: string
                    format: binary
                  description:
                    type: string
                  tags:
                    type: string
        responses:
          '200':
            description: OK
          '400':
            description: Bad Request
          '500':
            description: Internal Server Error
        """
        if 'file' not in request.files:
            return Response("No file attached", 400, headers=dict(request.headers)) # Wrong way
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
        image.comments = []
        image.likes = []
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
        """
        ---
        description: Get details of one image
        parameters:
          - $ref: '#/components/parameters/image'
        responses:
          '200':
            description: Data of single sensor with extended location info
            content:
              application/json:
                example:
                  data:
                    comments: []
                    created_at: "2023-04-16 11:24:17.160000"
                    description: "This is junge"
                    id: "643bb0b1cefdbc83c5d61ac0"
                    is_abused: false
                    likes: []
                    storage_id: "234462c1-a06e-46a0-9520-e063bcf2ce53.jpg"
                    tags:
                    - "tree"
                    - "nature"
                    - "woodland"
                    - "holiday"
                  error: null
                  message: null
          '404':
            description: The image was not found
        """
        print("No cached")
        try:
          response = Response()
          response.headers['Content-Type'] = "application/json"
          response.status = 200
          response.data = utils.wrap_response(data=viewmodels.convert_image(image))
          return response
        except Exception as e:
          print("Error: ", e)
          return Response(utils.wrap_error(error=str(e)), 500)
    
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