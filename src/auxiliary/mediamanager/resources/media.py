from flask import Flask, request, Response
from flask_restful import Api, Resource
from mongoengine import *

from io import BytesIO
from minio import Minio
from flask import make_response
from minio import Minio
from werkzeug.utils import secure_filename
from mediamanager import utils

class MediaCollection(Resource):
  def post(self):
      if 'file' not in request.files:
        return Response("No file attached", 400, headers=dict(request.headers)) # Wrong way
      file = request.files['file']
      filename = secure_filename(file.filename)
      if filename == '':
        return Response("No file attached", 400, headers=dict(request.headers))
      print(file.filename)
      if not file:
          return Response("No file attached", 400, headers=dict(request.headers))
      if not utils.allowed_file(filename):
          return Response("Format unaccepted", 400, headers=dict(request.headers))
      found = utils.minio_client.bucket_exists("images")
      if not found:
          utils.minio_client.make_bucket("images")
      else:
          print("Bucket 'images' already exists")

      file_size = len(file.stream.read())
      file.seek(0)
      generated_guid = utils.generate_guid()
      new_name = f'{generated_guid}{utils.get_file_extension(filename)}'
      minio_result = utils.minio_client.put_object(
          "images", new_name, file.stream, file_size
      )

      print(
          "created {0} object; etag: {1}, version-id: {2}".format(
              minio_result.object_name, minio_result.etag, minio_result.version_id,
          ),
      )
      
      return new_name

class MediaItem(Resource):
    def get(self, storage_id):
        # Retrieve the image data from MinIO
        try:
          image_data = utils.minio_client.get_object('images', storage_id).read()
        except Exception as err:
          print(err)
          return f"No file with this id exists. More details: {err}", 400

        # Create a Flask response with the image data
        response = make_response(image_data)

        # Set the Content-Type header to indicate the image file format
        response.headers.set('Content-Type', 'image/jpeg')

        # Set the Content-Disposition header to suggest that the image should be downloaded as a file
        # response.headers.set('Content-Disposition', 'attachment', filename='image.jpg')

        # Return the Flask response
        return response