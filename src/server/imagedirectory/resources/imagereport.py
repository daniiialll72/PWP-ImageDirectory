"""
This module provides the api facilities for the reporting the image.
"""
from flask import request, Response
from flask_restful import Resource
from datetime import datetime
from imagedirectory import models, utils
from imagedirectory.constants import TEST_USER_ID

class ReportedImageCollection(Resource):
    """
    Resource class for handling the creation of a reported image entry.
    """
    
    def post(self, image):
        """
        POST method for creating a reported image entry.

        Args:
            image (Image): Image object for which the report is being created.

        Returns:
            response (Response): Response object with status code and message.
        """
        
        print(image.description)
        if not request.json:
            return Response(status=415)
        reported_image = models.ReportedImage(
            user_id=TEST_USER_ID,
            image_id=image.id,
            reason=request.json["reason"],
            accepted=False,
            created_at=datetime.now()
            )
        reported_image.save()
        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status_code = 201
        response.data = utils.wrap_response(message="image reported")
        return response
