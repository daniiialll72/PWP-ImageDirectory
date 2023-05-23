"""
This module provides a set of converter functions which convert models to the view models.
"""
from imagedirectory.constants import MEDIA_MANAGER_URL

class User():
    """
    A class representing a user in the system.

    Attributes:
    - username (str): The username of the user.
    - email (str): The email of the user.
    - first_name (str): The first name of the user.
    - last_name (str): The last name of the user.
    - gender (str): The gender of the user.
    - password_hash (str): The hashed password of the user.
    """
    username = str
    email = str
    first_name = str
    last_name = str
    gender = str
    password_hash = str
    
class Image():
    """
    A class representing an image in the system.

    Attributes:
    - id (str): The ID of the image.
    - description (str): The description of the image.
    - tags (list): A list of tags associated with the image.
    - storage_id (str): The ID of the storage where the image is stored.
    - likes (list): A list of usernames of users who liked the image.
    - comments (list): A list of comments associated with the image.
    - created_at (str): The timestamp of when the image was created.
    - is_abused (bool): A flag indicating if the image has been flagged as abusive.
    """
    id = str
    description = str
    tags = list
    storage_id = str
    likes = list
    comments = list
    created_at = str
    is_abused = bool

def convert_users(users):
    """
    Converts a list of User objects to a list of dictionaries.

    Args:
    - users (list): A list of User objects.

    Returns:
    A list of dictionaries, with each dictionary representing a User object.
    """
    list = []
    for user in users:
        list.append(convert_user(user))
    
    return list

def convert_user(user):
    """
    Converts a User object to a dictionary.

    Args:
    - user (User): A User object.

    Returns:
    A dictionary representing the User object.
    """
    new = User()
    new.username = user.username
    new.email = user.email
    new.first_name = user.first_name
    new.last_name = user.last_name
    new.gender = user.gender
    new.password_hash = user.password_hash    
    return new

def convert_images(images):
    """
    Converts a list of images to a list of Image objects.
    
    Parameters:
    images (list): A list of images to be converted.
    
    Returns:
    list: A list of converted Image objects.
    """
    image_list = []
    for image in images:
        image_list.append(convert_image(image))
    return image_list

def convert_image(image):
    """
    Converts an image to an Image object.
    
    Parameters:
    image (object): The image to be converted.
    
    Returns:
    Image: The converted Image object.
    """
    new_image = Image()
    new_image.id = str(image.id)
    new_image.description = image.description
    new_image.tags = image.tags
    new_image.likes = image.likes
    new_image.comments = []
    for comment in image.comments:
        new_image.comments.append({ "id": str(comment.id), "user": str(comment.user_id.id), "text": comment.text})
    
    new_image.likes = []
    for like in image.likes:
        new_image.likes.append({ "user": str(like.user_id.id)})
    
    new_image.created_at = str(image.created_at)
    new_image.is_abused = image.is_abused
    new_image.url = f'{MEDIA_MANAGER_URL}/api/media/{image["file_content"]["storage_id"]}'
    
    return new_image