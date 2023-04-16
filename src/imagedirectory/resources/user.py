from flask import request, Response
from flask_restful import Resource
from imagedirectory import models
from imagedirectory import viewmodels
from mongoengine import *
from imagedirectory import utils

class UserCollection(Resource):
    def get(self):
        """Returns the game by name or id.
        ---
        description: Get the list of users
        responses:
          '200':
            description: List of users
            content:
              application/json:
                example:
                - name: test-sensor-1
                  model: uo-test-sensor
                  location: test-site-a
                - name: test-sensor-2
                  model: uo-test-sensor
                  location: null
        """
        try:
          users = models.User.objects
          response = Response()
          response.headers['Content-Type'] = "application/json"
          response.status = 200
          response.data = utils.wrap_response(data=viewmodels.convert_users(users))
          return response
        except Exception as e:
          print("Error: ", e)
          return Response(utils.wrap_response(data=str(e)), 200)

    def post(self):
        """
        ---
        description: Create a new user
        requestBody:
          description: JSON document that contains basic data for a new user
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Sensor'
              example:
                username: mkaheh
                email: kahe.mehrdad@gmail.com
                first_name: Mehrdad
                last_name: Kaheh
                password: 1234qwerty
                gender: male
        responses:
          '201':
            description: The user was created successfully
            headers:
            Location: 
              description: URI of the new user
              schema: 
                type: string
          '400':
            description: The request body was not valid
          '409':
            description: A sensor with the same name already exists
          '415':
            description: Wrong media type was used
        """
        if not request.json:
            return Response(status=415)
        
        username = request.json["username"]
        email = request.json["email"]
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        password = request.json["password"]
        gender = request.json["gender"]
        
        if not utils.validate_username(username):
            response = Response()
            response.status = 400
            response.data = utils.wrap_error(error = "username is invalid")
            return response
        
        if utils.check_username_exist(username):
            response = Response()
            response.status = 400
            response.data = utils.wrap_error(error = "username already exists")
            return response
        
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
            response = Response()
            response.status = 400
            response.data = utils.wrap_error(error = str(e))
            return response
        
        response = Response()
        response.headers['Location'] = f'/api/users/{user.username}/'
        response.headers['Content-Type'] = "application/json"
        response.status = 201
        response.data = utils.wrap_response(message="User created")
        return response
    
class UserItem(Resource):
    def get(self, user):
        """
        ---
        description: Get details of one user
        parameters:
          - $ref: '#/components/parameters/user'
        responses:
          '200':
            description: Data of single sensor with extended location info
            content:
              application/json:
                examples:
                  deployed-sensor:
                    description: A sensor that has been placed into a location
                    value:
                      name: test-sensor-1
                      model: uo-test-sensor
                      location:
                        name: test-site-a
                        latitude: 123.45
                        longitude: 123.45
                        altitude: 44.51
                        description: in some random university hallway
                  stored-sensor:
                    description: A sensor that lies in the storage, currently unused
                    value:
                      name: test-sensor-2
                      model: uo-test-sensor
                      location: null
          '404':
            description: The sensor was not found
        """
        return Response(user.to_json(), status=200, headers=dict(request.headers))