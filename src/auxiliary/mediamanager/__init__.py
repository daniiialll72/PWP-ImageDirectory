from flask import Flask
from flask_cors import CORS

def create_app(test_config=None):
    """
    Create Application method
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    CORS(app)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from mediamanager import api
    app.register_blueprint(api.api_bp)

    @app.route('/')
    def check():
        return 'Health check! The media manager app works!'

    return app
