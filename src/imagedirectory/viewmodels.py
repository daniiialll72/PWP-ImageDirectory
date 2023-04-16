
class User():
    username = str
    email = str
    first_name = str
    last_name = str
    gender = str
    password_hash = str

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