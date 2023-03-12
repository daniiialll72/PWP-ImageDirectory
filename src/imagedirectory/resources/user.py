from flask import request, Response
from flask_restful import Resource
from imagedirectory import models
from mongoengine import *

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