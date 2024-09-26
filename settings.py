import json

def change_post_per_page(user_id, option):
    with open(f'users/{user_id}.json', 'r+') as user_file:
        user_data = json.load(user_file)
        user_data["settings"]["post_per_page"] = option
        user_file.seek(0)
        json.dump(user_data, user_file, sort_keys=True, indent=4)
        user_file.truncate()

def change_log_off(user_id, option):
    with open(f'users/{user_id}.json', 'r+') as user_file:
        user_data = json.load(user_file)
        user_data["logoff_time"] = option
        user_file.seek(0)
        json.dump(user_data, user_file, sort_keys=True, indent=4)
        user_file.truncate()
        
def change_sidebar(user_id):
    with open(f'users/{user_id}.json', 'r+') as user_file:
        user_data = json.load(user_file)
        if user_data["settings"]["sidebar"] == True:
            user_data["settings"]["sidebar"] = False
        elif user_data["settings"]["sidebar"] == False:
            user_data["settings"]["sidebar"] = True
        user_file.seek(0)
        json.dump(user_data, user_file, sort_keys=True, indent=4)
        user_file.truncate()
        
def change_dark_mode(user_id):
    with open(f'users/{user_id}.json', 'r+') as user_file:
        user_data = json.load(user_file)
        if user_data["settings"]["dark_mode"] == True:
            user_data["settings"]["dark_mode"] = False
        elif user_data["settings"]["dark_mode"] == False:
            user_data["settings"]["dark_mode"] = True
        user_file.seek(0)
        json.dump(user_data, user_file, sort_keys=True, indent=4)
        user_file.truncate()
        
def get_user_settings(user_id):
    with open(f'users/{user_id}.json', 'r') as user_file:
        user_data = json.load(user_file)
        time = user_data["logoff_time"]
        settings = user_data["settings"]
        settings["time"] = time
        return settings
    
def get_user_post_per_page(user_id):
    with open(f'users/{user_id}.json', 'r') as user_file:
        user_data = json.load(user_file)
        return user_data["settings"]["post_per_page"]
    
def get_user_theme(user_id_data):
    with open(f'users/{user_id_data}.json', 'r') as user_file:
        user_data = json.load(user_file)
        return user_data["settings"]["dark_mode"]
    
def get_side_bar(user_id):
    with open(f'users/{user_id}.json', 'r') as user_file:
        user_data = json.load(user_file)
        return user_data["settings"]["sidebar"]