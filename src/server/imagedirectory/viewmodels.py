from imagedirectory.constants import MEDIA_MANAGER_URL

class User():
    username = str
    email = str
    first_name = str
    last_name = str
    gender = str
    password_hash = str
    
class Image():
    id = str
    description = str
    tags = list
    storage_id = str
    likes = list
    comments = list
    created_at = str
    is_abused = bool

def convert_users(users):
    list = []
    for user in users:
        list.append(convert_user(user))
    
    return list

def convert_user(user):
    new = User()
    new.username = user.username
    new.email = user.email
    new.first_name = user.first_name
    new.last_name = user.last_name
    new.gender = user.gender
    new.password_hash = user.password_hash    
    return new

def convert_images(images):
    image_list = []
    for image in images:
        image_list.append(convert_image(image))
    return image_list

def convert_image(image):
    new_image = Image()
    new_image.id = str(image.id)
    new_image.description = image.description
    new_image.tags = image.tags
    new_image.likes = image.likes
    new_image.comments = image.comments
    new_image.created_at = str(image.created_at)
    new_image.is_abused = image.is_abused
    new_image.url = f'{MEDIA_MANAGER_URL}/api/media/{image["file_content"]["storage_id"]}'
    
    return new_image