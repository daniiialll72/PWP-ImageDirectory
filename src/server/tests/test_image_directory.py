from imagedirectory import create_app, connect_db
import pytest
import tempfile
import os
import json
import io
from datetime import datetime

from imagedirectory.models import Image, ApiKey, User, FileContent
        
IMAGE_ID = ""

@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    config = {
        "TESTING": True
    }
    
    app = create_app(config)
    connect_db()
    _populate_db()
    
    yield app.test_client()
    
    os.close(db_fd)
    os.unlink(db_fname)
    
def _populate_db():
    # Remove all the records in the database
    Image.objects().delete()
    ApiKey.objects().delete()
    User.objects().delete()
    
    # Create user
    user = User()
    user.email = "John@gmail.com"
    user.username = "john"
    user.first_name = "John"
    user.last_name = "Doe"
    user.gender = "male"
    user.password_hash = "HashedPassword"
    user.save()
    
    
    # Create image
    image = Image()
    image.user_id = user.id
    image.description = "A cute rabbit"
    image.tags = "animal, cute, rabbit".replace(' ', '').split(',')
    image.created_at = datetime.now()
    image.file_content = FileContent(file_name="rabbit.jpg", storage_id="aaaabbbbccccdddd")
    image.save()
    
    IMAGE_ID = str(image.id)
    
    return

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

def test_hello_world():
    app = create_app()
    with app.test_client() as client:
        response = client.get('/hello')
        assert response.status_code == 200
        assert response.data == b'Hello, World!'
        
class TestUserCollection(object):
    RESOURCE_URL = "/api/users/"
    def test_get_expect_403(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 403
        
    def test_get_expect_200(self, client, auth):
        token = auth.get_key()
        resp = client.get(self.RESOURCE_URL, headers={"Api-Key": token})
        assert resp.status_code == 200
        
    def test_post_expect_403(self, client, auth):
        token = auth.get_key()
        resp = client.post(self.RESOURCE_URL)
        assert resp.status_code == 403
        
    def test_post_expect_400(self, client, auth):
        token = auth.get_key()
        resp = client.post(self.RESOURCE_URL, headers={"Api-Key": token})
        assert resp.status_code == 400
        
    def test_post_expect_200(self, client, auth):
        token = auth.get_key()
        payload = {
            "username": "mehrdad",
            "email": "mehrdad@gmail.com",
            "first_name": "Mehrdad",
            "last_name": "Kaheh",
            "password": "1234qwerty",
            "gender": "male"
        }
        resp = client.post(self.RESOURCE_URL, headers={"Api-Key": token}, json=payload)
        assert resp.status_code == 201
        assert resp.headers["Location"].endswith("mehrdad/")
        
class TestUserItems(object):
    RESOURCE_URL = "/api/users/john"
    def test_get_expect_400(self, client, auth):
        RESOURCE_URL_2 = self.RESOURCE_URL + "doe"
        resp = client.get(RESOURCE_URL_2)
        assert resp.status_code == 404

    def test_get_expect_200(self, client, auth):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        
class TestKeyCollection(object):
    RESOURCE_URL = "/api/key/"
    def test_post_expect_201(self, client):
        resp = client.post(self.RESOURCE_URL)
        assert resp.status_code == 201
        
class TestImageCollection(object):
    RESOURCE_URL = "/api/images/"
    
    def test_post_expect_201(self, client):
        form_data = {
            'tags': 'animal, rabbit',
            'description': 'this is a cute drawing of a rabbit',
        }
        
        form_data['file'] = (io.BytesIO(b"my file content"), 'rabbit.jpg')
        
        resp = client.post(self.RESOURCE_URL, data=form_data, content_type='multipart/form-data')
        assert resp.status_code == 201

    def test_post_expect_400(self, client):
        form_data = {
            'tags': 'animal, rabbit',
            'description': 'this is a cute drawing of a rabbit',
        }
                
        resp = client.post(self.RESOURCE_URL, data=form_data, content_type='multipart/form-data')
        assert resp.status_code == 400
        
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200

class TestImageItem(object):
    RESOURCE_URL = f"/api/images/{IMAGE_ID}"
    
    def test_get_expect_200(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
    print("****************")
    def test_get_expect_404(self, client):
        resp = client.get(self.RESOURCE_URL+"fs")
        assert resp.status_code == 404
    
    
