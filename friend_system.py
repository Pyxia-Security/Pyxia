import json

def check_if_friends(user_id, friend_id):
    with open(f"users/{user_id}.json", 'r') as user_info:
        data = json.load(user_info)
        if str(friend_id) in data["friends"]:
            return True
        else:
            return False
            
def read_friends(id):
    with open(f'users/{id}.json', 'r') as data:
        user_data = json.load(data)
        return user_data["friends"]
    
def get_user_profile(user_id):
    with open(f"users/{user_id}.json", 'r') as user_info:
        data = json.load(user_info)
        return data
    
def get_user_name(user_id):
    with open(f"users/{user_id}.json", 'r') as user:
        data = json.load(user)
        return data["username"]

def get_user_friend(user_id):
    with open(f"users/{user_id}.json", 'r') as user:
        data = json.load(user)
        return data["friends"]
    
def set_user_names(user_id):
    friend_data = get_user_friend(user_id)
    new_data = []
    for friend in friend_data:
        if str(friend) == str(user_id):
            pass
        else:
            friend_temp = get_user_name(friend)
            new_data.append([friend_temp, friend])
    return new_data