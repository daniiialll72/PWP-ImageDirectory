import requests
from imagedirectory.constants import MEDIA_MANAGER_URL

class MediaManager:
    def insertImage(self, file):
        url = f"{MEDIA_MANAGER_URL}/api/media/"
        print(url)
        files=[('file',(file.filename, file.stream, file.content_type))]
        response = requests.request("POST", url, files=files)
        print(response.text)
        return response.json()['data']
        
    def deleteImage(self, storage_id):
        url = f"{MEDIA_MANAGER_URL}/api/media/{storage_id}"
        response = requests.request("DELETE", url)
        print(response.text)
        if response.status_code != 200:
            return False
        else:
            return True