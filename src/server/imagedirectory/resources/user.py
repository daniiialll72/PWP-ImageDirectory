"""
This module provides the api facilities for the user resources.
"""
from flask import request, Response
from flask_restful import Resource
from mongoengine import errors

from imagedirectory.models import User
from imagedirectory import viewmodels, utils

class UserCollection(Resource):
    """
    Resource class for managing the Users.
    """
    
    @utils.require_key
    def get(self):
        """
        ---
        description: Get the list of users
        responses:
          '200':
            description: List of users
            content:
              application/json:
                example:
                  data:
                  - email: "mehrdad@gmail.com"
                    first_name: "Mehrdad"
                    gender: "male"
                    last_name: "Kaheh"
                    password_hash: "pbkdf2:sha256:260000$N33Rqt3K6Ha8MTz6..."
                    username: "mehrdad"
        """
        try:
            users = User.objects
            response = Response()
            response.headers['Content-Type'] = "application/json"
            response.status = 200
            response.data = utils.wrap_response(data=viewmodels.convert_users(users))
            return response
        except errors.MongoEngineException as error:
            print("Error: ", error)
            return Response(utils.wrap_response(data=str(error)), 400)

    @utils.require_key
    def post(self):
        """
        ---
        description: Create a new user
        requestBody:
          description: JSON document that contains basic data for a new user
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
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
        user = User(
            email = email,
            username = username,
            first_name = first_name,
            last_name = last_name,
            gender = gender,
            password_hash = utils.get_password_hash(password),
            )
        try:
            user.save()
        except errors.MongoEngineException as ex:
            response = Response()
            response.status = 400
            response.data = utils.wrap_error(error = str(ex))
            return response
        response = Response()
        response.headers['Location'] = f'/api/users/{user.username}/'
        response.headers['Content-Type'] = "application/json"
        response.status = 201
        response.data = utils.wrap_response(message="User created")
        return response

class UserItem(Resource):
    """
    Resource class for managing the single user.
    """
    def get(self, user):
        """
        ---
        description: Get details of one user
        parameters:
          - $ref: '#/components/parameters/user'
        responses:
          '200':
            description: List of users
            content:
              application/json:
                example:
                  data:
                  - email: "mehrdad@gmail.com"
                    first_name: "Mehrdad"
                    gender: "male"
                    last_name: "Kaheh"
                    password_hash: "pbkdf2:sha256:260000$N33Rqt3K6Ha8MTz6..."
                    username: "mehrdad"
          '404':
            description: The user was not found
        """
        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status = 200
        response.data = utils.wrap_response(data=viewmodels.convert_user(user))
        return response
      
    def patch(self, user):
        """
        ---
        description: Change the user details
        parameters:
          - $ref: '#/components/parameters/user'
        requestBody:
          description: JSON document that contains fields of user that can be modified
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
              example:
                first_name: John
                last_name: Doe
                gender: male
        responses:
          '200':
            description: Change the user details
            content:
              application/json:
                example:
                  data: null
                  error: null
                  message: yser has been modified
          '404':
            description: The image was not found
          '415':
            description: The media type format is not json
        """
        if not request.json:
            Response(status=415)
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        gender = request.json["gender"]
        
        if gender not in ["male", "female"]:
          response = Response()
          response.headers['Content-Type'] = "application/json"
          response.status = 400
          response.data = utils.wrap_error(error="Gender should be male or female")
          return response 

        user.first_name = first_name
        user.last_name = last_name
        user.gender = gender
        user.save()
        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status = 200
        response.data = utils.wrap_response(message="User has been modified")
        return response

