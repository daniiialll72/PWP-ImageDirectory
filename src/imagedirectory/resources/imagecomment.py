from flask import request, Response
from flask_restful import Resource
from imagedirectory import models
from mongoengine import *

TEST_USER_ID = "64099805f162b6c56e7ada81"

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