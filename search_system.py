import json
from friend_system import read_friends
from post_creator import load_friends_post, get_post_name, get_usrname_by_postid

def search_for(params, user_id):
    post_data = get_post_data4srch(user_id)
    posts = read_posts_search(post_data, params)
    final_post_data = add_usrnm_and_pstnm(posts)
    return final_post_data

def get_post_data4srch(user_id):
    friends = read_friends(user_id)
    friends_posts = load_friends_post(friends)
    with open('posts/total_post.json', 'r') as posts:
        post_data = json.load(posts)
        public_posts = post_data["posts"]["post"]
    master_post_list = friends_posts + public_posts
    return master_post_list

def read_posts_search(post_data, param):
    posts_with_info = []
    for data in post_data:
        with open(f'posts/{data}/post.json', 'r') as post:
            post_file_data = json.load(post)
            if param in post_file_data["description"].lower():
                posts_with_info.append(data)
            elif param in post_file_data["title"].lower():
                posts_with_info.append(data)
    return posts_with_info

def add_usrnm_and_pstnm(data):
    final_list = []
    for post in data:
        post_name = get_post_name(post)
        creator = get_usrname_by_postid(post)
        final_list.append([post, post_name, creator[1], creator[0]])
    return final_list
        
def search_for_user(user_name):
    found_users = []
    with open("users/users.json", 'r') as user_info:
        data = json.load(user_info)
        for user in data["users"]:
            if user_name in user[1].lower():
                found_users.append(user)
            elif user_name in user[0]:
                found_users.append(user[0])
    return found_users