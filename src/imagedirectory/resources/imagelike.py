from flask import request, Response
from flask_restful import Resource
from imagedirectory import models
from mongoengine import *
from datetime import datetime

TEST_USER_ID = "64099805f162b6c56e7ada81"

class ImageLikeCollection(Resource):
    def post(self, image):
        user = models.User.objects.get(id=TEST_USER_ID) # TODO: Should be changed with Authenticated user id
        for like in image.likes:
            if like.userId.id == user.id:
                previous_like = like
        if previous_like is not None:
            return Response("The record already exists", status=400)
        like = models.Like(userId=user.id, created=datetime.now())
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
