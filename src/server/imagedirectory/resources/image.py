"""
This module provides the api facilities for the image resource.
"""

from flask import request, Response
from flask_restful import Resource
from werkzeug.utils import secure_filename
from datetime import datetime
from mongoengine import errors

from imagedirectory import utils
from imagedirectory import cache
from imagedirectory import models
from imagedirectory import viewmodels
from imagedirectory.services.mediamanager import MediaManager

class ImageCollection(Resource):
    """
    Resource class for managing the images.
    """
    @cache.cached(timeout=30)
    def get(self):
        """
        ---
        description: Get the list of images
        responses:
          '200':
            description: List of images
            content:
              application/json:
                example:
                  data:
                    - comments: []
                      created_at: "2023-05-23 11:43:25.271000"
                      description: "A cute rabbit"
                      id: "646ca6dd52321cb454374db9"
                      is_abused: false
                      likes: []
                      tags:
                        - "animal"
                        - "cute"
                        - "rabbit"
                      url: "http://86.50.229.208:5001/api/media/aaaabbbbccccdddd"
                  error: null
                  message: null
          '400':
            description: error message
            content:
              application/json:
                example:
                  data: null
                  error: error message
                  message: null
        """
        print("No cached")
        try:
            images = models.Image.objects
            response = Response()
            response.headers['Content-Type'] = "application/json"
            response.status = 200
            response.data = utils.wrap_response(data=viewmodels.convert_images(images))
            return response
        except errors.MongoEngineException as ex:
            print("Error: ", ex)
            response = Response()
            response.headers['Content-Type'] = "application/json"
            response.status = 400
            response.data = utils.wrap_error(error=str(ex))
            return response

    # https://flask.palletsprojects.com/en/2.2.x/patterns/fileuploads/
    def post(self):
        """
        ---
        description: Insert a new image
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
          '201':
            description: OK
            content:
              application/json:
                example:
                  data: null
                  message: A new image added
                  error: null
          '400':
            description: Bad Request
            content:
              application/json:
                example:
                  data: null
                  message: null
                  error: error message
        """
        mediamanger = MediaManager()
        print("file type is: " , type(request.files['file']))
        result = mediamanger.insertImage(request.files['file'])
        file = request.files['file']
        filename = secure_filename(file.filename)
        tags_string = request.form.get('tags')
        tags_list = tags_string.replace(' ', '').split(',')
        image = models.Image()
        image.description = request.form.get('description')
        image.tags = tags_list
        image.created_at = datetime.now()
        image.file_content = models.FileContent(file_name=filename, storage_id=result)
        try:
            print(image.description)
            image.save()
        except errors.MongoEngineException as error:
            response = Response()
            response.headers['Content-Type'] = "application/json"
            response.status = 400
            response.data = utils.wrap_error(error=str(error))
            return response

        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status = 201
        response.data = utils.wrap_response(message="A new image added")
        return response

class ImageItem(Resource):
    """
    Resource class for managing the image items.
    """
    @cache.cached(timeout=30)
    def get(self, image):
        """
        ---
        description: Get details of one image
        parameters:
          - $ref: '#/components/parameters/image'
        responses:
          '200':
            description: Data of an image
            content:
              application/json:
                example:
                  data:
                    - comments: []
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
        except errors.MongoEngineException as ex:
            print("Error: ", ex)
            return Response(utils.wrap_error(error=str(ex)), 400)

    def delete(self, image):
        """
        ---
        description: Delete an image
        parameters:
          - $ref: '#/components/parameters/image'
        responses:
          '200':
            description: Delete an image
            content:
              application/json:
                example:
                  data: null
                  error: null
                  message: Image is deleted
          '404':
            description: The image was not found
        """
        try:
            mediamanger = MediaManager()
            mediamanger.deleteImage(image.file_content.storage_id)
            image.delete()
            response = Response()
            response.headers['Content-Type'] = "application/json"
            response.status = 200
            response.data = utils.wrap_response(message="Image has been deleted")
            return response
        except errors.MongoEngineException as ex:
            print("Error: ", ex)
            response = Response()
            response.headers['Content-Type'] = "application/json"
            response.status = 400
            response.data = utils.wrap_error(error="Image has been already deleted")
            return response

    def patch(self, image):
        """
        ---
        description: Change the image details
        parameters:
          - $ref: '#/components/parameters/image'
        requestBody:
          description: JSON document that contains fields of image that can be modified
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Image'
              example:
                description: new description
                tags: apple
        responses:
          '200':
            description: Change the image details
            content:
              application/json:
                example:
                  data: null
                  error: null
                  message: image has been modified
          '404':
            description: The image was not found
          '415':
            description: The media type format is not json
        """
        if not request.json:
            Response(status=415)
        description = request.json["description"]
        tags_string = request.json["tags"]

        image.description = description
        image.tags = tags_string.replace(' ', '').split(',')
        image.save()
        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status = 200
        response.data = utils.wrap_response(message="Image has been modified")
        return response
