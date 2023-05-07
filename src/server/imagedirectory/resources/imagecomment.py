"""
This module provides the api facilities for the image comment resource.
"""
from flask import request, Response
from flask_restful import Resource
from imagedirectory import models
from imagedirectory.constants import TEST_USER_ID
from imagedirectory import utils

class ImageCommentCollection(Resource):
    """
    Resource class for managing the image collections.
    """
    def post(self, image):
        """
        ---
        description: Add comment to the image
        parameters:
          - $ref: '#/components/parameters/image'
        requestBody:
          description: JSON document that contains fields of a new comment
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ImageComment'
              example:
                text: your comment
        responses:
          '200':
            description: Comment is added
            content:
              application/json:
                example:
                  data: null
                  error: null
                  message: Comment is added
          '404':
            description: The image was not found
            content:
              application/json:
                example:
                  data: null
                  error: The image was not found
                  message: null
          '415':
            description: The media type format is not json
        """
        if not request.json:
            Response(status=415)
        text = request.json["text"]
        user = models.User.objects.get(id=TEST_USER_ID)
        comment = models.Comment(user_id=user.id, text=text)
        image.comments.append(comment)
        image.save()
        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status = 201
        response.data = utils.wrap_response(message="comment added")
        return response
    
class ImageCommentItem(Resource):
    """
    Resource class for managing the image items.
    """
    def delete(self, image, comment_id):
        """
        ---
        description: Delete the comment
        parameters:
          - $ref: '#/components/parameters/image'
          - name: comment_id
            in: path
            schema:
              type: string
        responses:
          '200':
            description: Comment is deleted
            content:
              application/json:
                example:
                  data: null
                  error: null
                  message: Comment is deleted
          '404':
            description: The image or comment was not found
            content:
              application/json:
                example:
                  data: null
                  error: The image or comment was not found
                  message: null
        """
        previous_comment = None
        for comment in image.comments:
            print(str(comment.id))
            print(str(comment_id))
            if str(comment.id) == comment_id:
                previous_comment = comment
        if previous_comment is None:
            response = Response()
            response.headers['Content-Type'] = "application/json"
            response.status = 404
            response.data = utils.wrap_error(error="The image or comment was not found")
            return response
        image.update(pull__comments=previous_comment)
        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status = 200
        response.data = utils.wrap_response(message="comment deleted")
        return response