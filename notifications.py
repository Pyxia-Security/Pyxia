import json

def check_friend_notifications(user_id):
    with open(f'users/{user_id}.json', 'r') as user:
        user_data = json.load(user)
        friend_requests = len(user_data["requests"])
    return friend_requests