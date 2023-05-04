from flask import request, Response
from flask_restful import Resource
from imagedirectory import models
from mongoengine import *
from imagedirectory.constants import *
from datetime import datetime
from imagedirectory import utils

class ReportedImageCollection(Resource):
    def post(self, image):
        print(image.description)
        if not request.json:
            Response(status=415)
            
        reportedImage = models.ReportedImage(
            user_id=TEST_USER_ID,
            image_id=image.id,
            reason=request.json["reason"],
            accepted=False,
            created_at=datetime.now()
            )
        reportedImage.save()
        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status = 201
        response.data = utils.wrap_response(message="image reported")
        return response
