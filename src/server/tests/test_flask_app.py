from imagedirectory import create_app
import pytest
import tempfile
import os
import json

from imagedirectory.models import Image, ApiKey

def test_hello_world():
    app = create_app()
    with app.test_client() as client:
        response = client.get('/hello')
        assert response.status_code == 200
        assert response.data == b'Hello, World!'
        
@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "TESTING": True
    }
    
    app = create_app(config)
    _populate_db()
    
    yield app.test_client()
    
    os.close(db_fd)
    os.unlink(db_fname)
    
def _populate_db():
    return
    # for i in range(1, 4):
    #     s = Image(
    #         name="test-sensor-{}".format(i),
    #         model="testsensor"
    #     )
    #     db.session.add(s)
        
    # db_key = ApiKey(
    #     key=ApiKey.key_hash(TEST_KEY),
    #     admin=True
    # )
    # db.session.add(db_key)        
    # db.session.commit()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def get_key(self):
        response = self._client.post('/api/key/')
        token = json.loads(response.data.decode())['data']
        return token

@pytest.fixture
def auth(client) -> AuthActions:
    return AuthActions(client)

class TestUserCollection(object):
    RESOURCE_URL = "/api/users/"
    def test_get_expect_403(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 403
        
    def test_get_expect_200(self, client, auth):
        token = auth.get_key()
        resp = client.get(self.RESOURCE_URL, headers={"Api-Key": token})
        assert resp.status_code == 200
        
class TestKeyCollection(object):
    RESOURCE_URL = "/api/key/"
    def test_post_expect_201(self, client):
        resp = client.post(self.RESOURCE_URL)
        assert resp.status_code == 201
        
class TestImageCollection(object):
    RESOURCE_URL = "/api/images/"
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200

    # def test_post(self, client):
    #     valid = _get_sensor_json()
        
    #     # test with wrong content type
    #     resp = client.post(self.RESOURCE_URL, data="notjson")
    #     assert resp.status_code in (400, 415)
        
    #     # test with valid and see that it exists afterward
    #     resp = client.post(self.RESOURCE_URL, json=valid)
    #     assert resp.status_code == 201
    #     assert resp.headers["Location"].endswith(self.RESOURCE_URL + valid["name"] + "/")
    #     resp = client.get(resp.headers["Location"])
    #     assert resp.status_code == 200
        
    #     # send same data again for 409
    #     resp = client.post(self.RESOURCE_URL, json=valid)
    #     assert resp.status_code == 409
        
    #     # remove model field for 400
    #     valid.pop("model")
    #     resp = client.post(self.RESOURCE_URL, json=valid)
    #     assert resp.status_code == 400