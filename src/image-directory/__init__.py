import os
from flask import Flask, request, Response
import pprint
from flask_restful import Api, Resource
from . import models
from mongoengine import *
from minio import Minio
from werkzeug.utils import secure_filename
import uuid
from werkzeug.routing import BaseConverter
from werkzeug.exceptions import NotFound
import datetime
import json
import logging

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s]: {} %(levelname)s %(message)s'.format(os.getpid()),
    datefmt='%Y-%m-%d %H:%M:%S', handlers=[logging.StreamHandler()])

    logger = logging.getLogger()

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
    
    minio_client = Minio(
        "86.50.229.208:9000",
        access_key="8UQvmZYlLMmbdGw4",
        secret_key="VxI9Ig0huEvN07seO168TY6E3eRDZUge",
        secure=False
    )

    ALLOWED_EXTENSIONS = {'jpg', 'png'}
    TEST_USER_ID = "64099805f162b6c56e7ada81"

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    from . import api

    return app