from flask import Flask
from .extensions import mongo

app = Flask(__name__)

@app.route('/')
def index():
    # user_collection = mongo.db.users
    return 'App works!'