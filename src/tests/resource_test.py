# import json
# import os
# import pytest
# import tempfile
# import time
# from datetime import datetime
# from flask.testing import FlaskClient
# from jsonschema import validate
# from sqlalchemy.engine import Engine
# from sqlalchemy import event
# from sqlalchemy.exc import IntegrityError, StatementError
# from werkzeug.datastructures import Headers

# from imagedirectory import create_app

# @pytest.fixture
# def client():
#     config = {
#         "TESTING": True
#     }
#     app = create_app(config)
#     yield app.test_client()

# class TestSensorCollection(object):
    
#     RESOURCE_URL = "/api/sensors/"

#     def test_get(self, client):
#         resp = client.get(self.RESOURCE_URL)
#         assert resp.status_code == 200
#         body = json.loads(resp.data)
#         _check_namespace(client, body)
#         _check_control_post_method("senhub:add-sensor", client, body)
#         assert len(body["items"]) == 3
#         for item in body["items"]:
#             _check_control_get_method("self", client, item)
#             _check_control_get_method("profile", client, item)

#     def test_post(self, client):
#         valid = _get_sensor_json()
        
#         # test with wrong content type
#         resp = client.post(self.RESOURCE_URL, data="notjson")
#         assert resp.status_code in (400, 415)
        
#         # test with valid and see that it exists afterward
#         resp = client.post(self.RESOURCE_URL, json=valid)
#         assert resp.status_code == 201
#         assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["name"] + "/")
#         resp = client.get(resp.headers["Location"])
#         assert resp.status_code == 200
        
#         # send same data again for 409
#         resp = client.post(self.RESOURCE_URL, json=valid)
#         assert resp.status_code == 409
        
#         # remove model field for 400
#         valid.pop("model")
#         resp = client.post(self.RESOURCE_URL, json=valid)
#         assert resp.status_code == 400
        