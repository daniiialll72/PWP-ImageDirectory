from flask import request, Response
from flask_restful import Resource
from imagedirectory import models
from mongoengine import *
from imagedirectory import utils

class UserCollection(Resource):
    def get(self):
        users = models.User.objects
        return Response(users.to_json(), 200, headers=dict(request.headers))

    def post(self):
        if not request.json:
            return Response(status=415)
        
        username = request.json["username"]
        email = request.json["email"]
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        password = request.json["password"]
        gender = request.json["gender"]
        
        if not utils.validate_username(username):
            return Response("username is invalid", status=400)
        
        if utils.check_username_exist(username):
            return Response("username already exists", status=400)
        
        user = models.User(
            email = email,
            username = username,
            first_name = first_name,
            last_name = last_name,
            gender = gender,
            password_hash = utils.get_password_hash(password),
            )
        try:
            user.save()
        except Exception as e:
            return Response(str(e), 400)
        return Response("user created", 201, headers=dict(request.headers))
    
class UserItem(Resource):
    def get(self, user):
        return Response(user.to_json(), status=200, headers=dict(request.headers))