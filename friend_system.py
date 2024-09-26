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
            new_data.append([friend_temp, friend, get_pfp(friend)])
    return new_data

def remove_friend(current_user_id, friend_user_id):
    with open(f"users/{friend_user_id}.json", 'r+') as friend_file:
        friend_data = json.load(friend_file)
        friend_data["friends"].remove(str(current_user_id))
        friend_file.seek(0)
        json.dump(friend_data, friend_file, sort_keys=True, indent=4)
        friend_file.truncate()
    with open(f"users/{current_user_id}.json", 'r+') as user:
        user_data = json.load(user)
        user_data["friends"].remove(friend_user_id)
        user.seek(0)
        json.dump(user_data, user, sort_keys=True, indent=4)
        user.truncate()
        
def accept_friend_request(user_id, friend_user_id):
    with open(f"users/{friend_user_id}.json", 'r+') as friend:
        friend_data = json.load(friend)
        friend_data["friends"].append(str(user_id))
        friend_data["requested"].remove(str(user_id))
        friend.seek(0)
        json.dump(friend_data, friend, sort_keys=True, indent=4)
        friend.truncate()
    with open(f'users/{user_id}.json', 'r+') as user:
        user_data = json.load(user)
        user_data["friends"].append(str(friend_user_id))
        user_data["requests"].remove(str(friend_user_id))
        user.seek(0)
        json.dump(user_data, user, sort_keys=True, indent=4)
        user.truncate()
        
def deny_friend_request(user_id, friend_user_id):
    with open(f"users/{friend_user_id}.json", 'r+') as friend:
        friend_data = json.load(friend)
        friend_data["requested"].remove(str(user_id))
        friend.seek(0)
        json.dump(friend_data, friend, sort_keys=True, indent=4)
        friend.truncate()
    with open(f'users/{user_id}.json', 'r+') as user:
        user_data = json.load(user)
        user_data["requests"].remove(str(friend_user_id))
        user.seek(0)
        json.dump(user_data, user, sort_keys=True, indent=4)
        user.truncate()
        
def request_friend(user_id, friend_user_id):
    with open(f"users/{friend_user_id}.json", 'r+') as friend:
        friend_data = json.load(friend)
        friend_data["requests"].append(str(user_id))
        friend.seek(0)
        json.dump(friend_data, friend, sort_keys=True, indent=4)
        friend.truncate()
    with open(f'users/{user_id}.json', 'r+') as user:
        user_data = json.load(user)
        user_data["requested"].append(str(friend_user_id))
        user.seek(0)
        json.dump(user_data, user, sort_keys=True, indent=4)
        user.truncate()
        
def check_if_already_requested(user_id, friend_user_id):
    with open(f"users/{friend_user_id}.json", 'r') as friend:
        friend_data = json.load(friend)
        if user_id in friend_data["requests"]:
            in_requests = True
        else:
            in_requests = False
    with open(f'users/{user_id}.json', 'r') as user:
        user_data = json.load(user)
        if user_id in user_data["requested"]:
            in_requested = True
        else:
            in_requested = False
    if in_requests == False or in_requested == False:
        if in_requests == False and in_requests == False:
            return False
        if in_requests == False:
            with open(f"users/{friend_user_id}.json", 'r+') as friend:
                friend_data = json.load(friend)
                friend_data["requests"].append(user_id)
                friend.seek(0)
                json.dump(friend_data, friend, sort_keys=True, indent=4)
                friend.truncate()
        elif in_requested == False:
            with open(f'users/{user_id}.json', 'r+') as user:
                user_data = json.load(user)
                user_data["requested"].append(friend_user_id)
                user.seek(0)
                json.dump(user_data, user, sort_keys=True, indent=4)
                user.truncate()
        return "modified"
    else:
        return True
    
def check_if_requested(user_id, friend_user_id):
    in_requested = False
    in_data = False
    print("In requested", in_requested)
    print("In data", in_data)
    with open(f"users/{friend_user_id}.json", 'r') as friend:
        friend_data = json.load(friend)
        print("friend data\n", friend_data)
        if user_id in friend_data["requested"]:
            in_data = True
        else:
            print("doesn't seem to be in friend_data requests")
    with open(f'users/{user_id}.json', 'r') as user:
        user_data = json.load(user)
        if friend_user_id in user_data["requests"]:
            in_requested = True
        else:
            print("doesn't seem to be in user_data")
    if in_requested == True and in_data == True:
        return "requested"
    else:
        return "not_requested"
    
def read_requests(user_id):
    with open(f'users/{user_id}.json', 'r') as user:
        data = json.load(user)
        request_user_ids = data["requests"]
        if request_user_ids == "" or request_user_ids == []:
            return []
        user_names = []
        for user in request_user_ids:
            name = get_user_name(user)
            user_names.append([user, name])
        return user_names
    
def read_requests_not_modify(user_id):
    with open(f'users/{user_id}.json', 'r') as user:
        data = json.load(user)
        request_user_ids = data["requests"]
        if request_user_ids == "" or request_user_ids == []:
            return []
        return request_user_ids
    
def read_requested_not_modify(user_id):
    with open(f'users/{user_id}.json', 'r') as user:
        data = json.load(user)
        request_user_ids = data["requested"]
        if request_user_ids == "" or request_user_ids == []:
            return []
        return request_user_ids
    
def check_if_requested_woutadd(user_id, friend_id):
    requested = read_requests_not_modify(friend_id)
    req_friend = False
    if str(user_id) in requested:
        req_friend = True
    req_as_user = False
    requested2 = read_requested_not_modify(user_id)
    if str(friend_id) in requested2:
        req_as_user = True
    if req_as_user == True and req_friend == True:
        return True
    else:
        return False
    
def unsend_friend_request(user_id, friend_user_id):
    with open(f"users/{friend_user_id}.json", 'r+') as friend:
        friend_data = json.load(friend)
        friend_data["requests"].remove(str(user_id))
        friend.seek(0)
        json.dump(friend_data, friend, sort_keys=True, indent=4)
        friend.truncate()
    with open(f'users/{user_id}.json', 'r+') as user:
        user_data = json.load(user)
        user_data["requested"].remove(str(friend_user_id))
        user.seek(0)
        json.dump(user_data, user, sort_keys=True, indent=4)
        user.truncate()
        
def get_pfp(user_id):
    with open(f'users/{user_id}.json', 'r') as user_file:
        user_info = json.load(user_file)
        custom_pfp = user_info["custom_pfp"]
        pfp_type = user_info["pfp_type"]
        return [custom_pfp, f"pfp/{user_id}{pfp_type}"]