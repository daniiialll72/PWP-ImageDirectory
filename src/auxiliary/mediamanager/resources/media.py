"""
This module provides a set of functions and utilities.
"""
from flask import request, Response
from flask_restful import Resource
from mongoengine import *
from flask import make_response
from werkzeug.utils import secure_filename

from mediamanager import utils

class MediaCollection(Resource):
    def post(self):
        """
        Post an image into storage based on its storage ID.
        
        Returns
        -------
        flask.Response
            The image file as a response object with the appropriate content type.
        """
        if 'file' not in request.files:
            return Response("No file attached", 400, headers=dict(request.headers)) # Wrong way TODO
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
        
        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status = 201
        response.data = utils.wrap_response(data=new_name)
        return response

class MediaItem(Resource):
    def get(self, storage_id):
        """
        Retrieve an image from storage based on its storage ID.

        Parameters
        ----------
        storage_id : str
            The ID of the image in the storage.

        Returns
        -------
        flask.Response
            The image file as a response object with the appropriate content type.
        """
        try:
            image_data = utils.minio_client.get_object('images', storage_id).read()
        except Exception as err:
            print(err)
            return f"No file with this id exists.", 400
        response = make_response(image_data)
        response.headers.set('Content-Type', 'image/jpeg')
        return response

    def delete(self, storage_id):
        """
        Delete an image from storage based on its storage ID.

        Parameters
        ----------
        storage_id : str
            The ID of the image in the storage.

        Returns
        -------
        flask.Response
            A response indicating the success or failure of the deletion operation.
        """
        try:
            utils.minio_client.remove_object("images", storage_id)
        except Exception as err:
            print(err)
            return f"No file with this id exists.", 400

        response = Response()
        response.headers['Content-Type'] = "application/json"
        response.status = 200
        response.data = utils.wrap_response(message="Image has been deleted")
        return response