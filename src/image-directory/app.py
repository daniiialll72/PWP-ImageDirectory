from flask import Flask, request, Response
import pprint
from flask_restful import Api, Resource
from . import models
from mongoengine import *

app = Flask(__name__)

# Connect to MongoDB
username = 'admin'
password = '1234qwerty'
server = '86.50.229.208'
db_name = 'image_directory'
uri = f'mongodb://{username}:{password}@{server}:27017/{db_name}?authSource=admin&retryWrites=true&w=majority'
connect(db=db_name, 
        username=username, 
        password=password, 
        host=uri)

api = Api(app)

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
        return Response(user.to_json(), 200, headers=dict(request.headers))

api.add_resource(UserCollection, "/api/users/")