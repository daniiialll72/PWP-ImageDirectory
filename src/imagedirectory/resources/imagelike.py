from flask import request, Response
from flask_restful import Resource
from imagedirectory import models
from mongoengine import *
from datetime import datetime
from imagedirectory.constants import TEST_USER_ID
from imagedirectory import utils


class ImageLikeCollection(Resource):
    def post(self, image):
        user = models.User.objects.get(id=TEST_USER_ID) # TODO: Should be changed with Authenticated user id
        previous_like = None
        for like in image.likes:
            if like.userId.id == user.id:
                previous_like = like
        if previous_like is not None:
            return Response("The record already exists", status=400)
        like = models.Like(user_id=user.id, created=datetime.now())
        image.likes.append(like)
        image.save()
        return Response(status=201)
    
    def delete(self, image):
        user = models.User.objects.get(id=TEST_USER_ID) # TODO: Should be changed with Authenticated user id
        previous_like = None
        for like in image.likes:
            if like.user_id.id == user.id:
                previous_like = like
        if previous_like is None:
            return Response("No record exists", status=400)
        image.update(pull__likes=previous_like)
        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status = 200
        response.data = utils.wrap_response(message="image liked")
        return response
        # return Response(status=200)

