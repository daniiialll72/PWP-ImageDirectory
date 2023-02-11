from flask import Flask
from .extensions import mongo

def create_app(configuartion_object='app.settings'):
    app = Flask(__name__)
    app.config.from_object(configuartion_object)
    mongo.init_app(app)
    return app
