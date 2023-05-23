"""
This module provides the api facilities for managing the api keys.
"""
from flask import Response
from flask_restful import Resource
import secrets

from imagedirectory import models, utils

class APIKeyCollection(Resource):
    """
    Resource class for handling the creation of a reported image entry.
    """

    def post(self):
        """
        ---
        description: Create a new api key
        responses:
          '200':
            description: Create a new api key
        """
        token = secrets.token_urlsafe()
        key_hash = models.ApiKey.key_hash(token).hex()
        apikey = models.ApiKey(
            key = key_hash
            )
        apikey.save()
        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status_code = 201
        response.data = utils.wrap_response(message="new api key generated", data=token)
        return response
