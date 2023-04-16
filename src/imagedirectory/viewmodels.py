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
        new = User()
        new.username = user.username
        new.email = user.email
        new.first_name = user.first_name
        new.last_name = user.last_name
        new.gender = user.gender
        new.password_hash = user.password_hash
        
        list.append(new)
    
    return list

def convert_images(images):
    image_list = []
    for image in images:
        new_image = Image()
        print(image.created_at)
        new_image.id = str(image.id)
        new_image.description = image.description
        new_image.tags = image.tags
        new_image.storage_id = image["file_content"]["storage_id"]
        new_image.likes = image.likes
        new_image.comments = image.comments
        new_image.created_at = str(image.created_at)
        new_image.is_abused = image.is_abused
        
        image_list.append(new_image)
    
    return image_list