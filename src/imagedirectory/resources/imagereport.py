from flask import request, Response
from flask_restful import Resource
from imagedirectory import models
from mongoengine import *
from imagedirectory.constants import *
from datetime import datetime

class ReportedImageCollection(Resource):
    def post(self, image):
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
        return Response(status=201)