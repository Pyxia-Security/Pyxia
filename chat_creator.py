import sys, random, json
from pathlib import Path

def chat_room_id_creator():
    random_num = random.randint(0, sys.maxsize)
    path = Path(f'/chat/{random_num}')
    if path.exists == True:
        while path.exists == True:
            random_num = random.randint(0,sys.maxsize)
            if path.exists == True:
                break
    return random_num

def check_if_exists_chat(chat_id):
    file_path = Path(f"chat/{chat_id}")
    if file_path.exists():
        return "exists"
    else:
        return "notexist"

def create_chat_room(user_1, user_2, chat_name):
    cr_id = chat_room_id_creator()
    try:
        file_path = Path(f"chat/{cr_id}")
        file_path.mkdir(exist_ok=False)
    except FileExistsError:
        while True:
            cr_id = chat_room_id_creator
            try:
                file_path = Path(f"chat/{cr_id}")
                file_path.mkdir(exist_ok=False)
                break
            except FileExistsError:
                pass
    with open(f'chat/{cr_id}/chat.json', 'w') as chat:
        data = {}
        data["chat_name"] = chat_name,
        data["users"] = [user_1, user_2]
        data["messages"] = []
        chat.seek(0)
        json.dump(data, chat, sort_keys=True, indent=4)
        chat.truncate()
    add_user_to_chat(user_1, cr_id, chat_name)
    add_user_to_chat(user_2, cr_id, chat_name)
    return cr_id
       
def add_message(chat_id, sender_id, sender, message):
    try:
        with open(f'chat/{chat_id}/chat.json', 'r+') as chat:
            data = json.load(chat)
            chat_message = [
                sender_id,
                sender,
                message
            ]
            data["messages"].append(chat_message)
            chat.seek(0)
            json.dump(data, chat, sort_keys=True, indent=4)
            chat.truncate()
            return ""
    except FileNotFoundError:
        return "noexistingchat"
    
def read_messages(chat_id):
    try:
        with open(f'chat/{chat_id}/chat.json', 'r') as chat:
            messages = json.load(chat)
            return messages["messages"]
    except FileNotFoundError:
        return "noexistingchat"
    
def read_user_chats(user_id):
    with open(f'users/{user_id}.json', 'r') as user:
        data = json.load(user)
        rooms = data["chat_rooms"]
        return rooms
    
def add_user_to_chat(user_id, chat_room, chat_name):
    with open(f'users/{user_id}.json', 'r+') as user:
        data = json.load(user)
        data["chat_rooms"].append([str(chat_room), chat_name])
        user.seek(0)
        json.dump(data, user, sort_keys=True, indent=4)
        user.truncate()
        
def check_if_user_can_read(user_id, chat_id):
    with open(f'users/{user_id}.json', 'r') as user:
        data = json.load(user)
        chats = data["chat_rooms"]
        for chat in chats:
            if str(chat[0]) == str(chat_id):
                return "can_read"
        return "cannot_read"
    
def get_chat_name(chat_id):
    with open(f'chat/{chat_id}/chat.json', 'r') as chat:
        data = json.load(chat)
        return data["chat_name"]
    
def add_user_conversation_to_user_list(user_id, friend_id):
    with open(f'users/{user_id}.json', 'r+') as user:
        data = json.load(user)
        data["conversation_with"].append(str(friend_id))
        user.seek(0)
        json.dump(data, user, sort_keys=True, indent=4)
        user.truncate()
    with open(f'users/{friend_id}.json', 'r+') as user:
        data = json.load(user)
        data["conversation_with"].append(str(user_id))
        user.seek(0)
        json.dump(data, user, sort_keys=True, indent=4)
        user.truncate()
        
def check_user_conversation_list(user_id, friend_id):
    with open(f'users/{user_id}.json', 'r+') as user:
        data = json.load(user)
        if str(friend_id) in data["conversation_with"]:
            return "already_exists"
        else:
            return "doesnt_exist"