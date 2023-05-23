"""
This module provides the api facilities for the image like resource.
"""
from flask import Response
from flask_restful import Resource
from imagedirectory import models
from datetime import datetime
from imagedirectory.constants import TEST_USER_ID
from imagedirectory import utils

class ImageLikeCollection(Resource):
    def post(self, image):
        """
        ---
        description: Like to the image
        parameters:
          - $ref: '#/components/parameters/image'
        responses:
          '200':
            description: Image is liked
            content:
              application/json:
                example:
                  data: null
                  error: null
                  message: Image is liked
          '404':
            description: The image was not found
            content:
              application/json:
                example:
                  data: null
                  error: The image was not found
                  message: null
        """
        user = models.User.objects.first()
        previous_like = None
        for like in image.likes:
            if like.user_id.id == user.id:
                previous_like = like
        if previous_like is not None:
            response = Response()
            response.headers['Content-Type'] = "application/json"
            response.status = 400
            response.data = utils.wrap_error(error="The image was already liked")
            return response
        like = models.Like(user_id=user.id, created=datetime.now())
        image.likes.append(like)
        image.save()
        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status = 201
        response.data = utils.wrap_response(message="Image is liked")
        return response

    def delete(self, image):
        """
        ---
        description: remove the like from image
        parameters:
          - $ref: '#/components/parameters/image'
        responses:
          '200':
            description: Like is deleted
            content:
              application/json:
                example:
                  data: null
                  error: null
                  message: Like is deleted
          '404':
            description: The image was not found
            content:
              application/json:
                example:
                  data: null
                  error: The image was not found
                  message: null
        """
        user = models.User.objects.first()
        previous_like = None
        for like in image.likes:
            if like.user_id.id == user.id:
                previous_like = like
        if previous_like is None:
            response = Response()
            response.headers['Content-Type'] = "application/json"
            response.status = 404
            response.data = utils.wrap_error(error="No record exists")
            return response
        image.update(pull__likes=previous_like)
        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status = 200
        response.data = utils.wrap_response(message="image liked")
        return response
