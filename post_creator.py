#!/usr/bin/env python3
import json, pyclamd, magic, random
from friend_system import read_friends
from pathlib import Path

def total_posts():
    with open('posts/total_post.txt', 'r') as post:
        return post.read()
    
def total_clips():
    with open('posts/clips/total_clips.txt', 'r') as clip:
        return clip.read()

def change_post_total_by_one():
    with open('posts/total_post.txt', 'r') as post:
        total = int(post.read())
        
    with open('posts/total_post.txt', 'w') as post:
        total += 1
        post.write(str(total))
        
def change_clip_total_by_one():
    with open('posts/clips/total_clips.txt', 'r') as clip:
        total = int(clip.read())
        
    with open('posts/clips/total_clips.txt', 'w') as clip:
        total += 1
        clip.write(str(total))
        
def change_post_total_by_minus_one():
    with open('posts/total_post.txt', 'r') as post:
        total = int(post.read())
        
    with open('posts/total_post.txt', 'w') as post:
        total -= 1
        post.write(str(total))

def scan_file(file_path):
    cd = pyclamd.ClamdAgnostic()
    result = cd.scan_file(file_path)
    return result

def scan_upload(file_path):
    scan_result = scan_file(file_path)
    if scan_result:
        return "malware"
    else:
        return "clean"
    
def create_list(id, title, desc, user, userid, privacy, images, total_images, age_rating, clips, clips_list):
    created_list = {
        "post_id": id,
        "title": title,
        "description": desc,
        "likes": None,
        "liked": None,
        "bookmarked": None,
        "user": user,
        "user_id": userid,
        "privacy": privacy,
        "images": images,
        "total_images": total_images,
        "age_rating": age_rating,
        "clips": clips,
        "clips_list": clips_list
    }
    return created_list

def create_clips_template(clips_list):
    created_list = {
        "post_id": clips_list["post_id"],
        "title": clips_list["title"],
        "description": clips_list["description"],
        "likes": None,
        "liked": None,
        "bookmarked": None,
        "user": clips_list["user"],
        "user_id": clips_list["user_id"],
        "privacy": clips_list["privacy"],
        "age_rating": clips_list["age_rating"],
        "clips_list": clips_list["clips_list"]
    }
    return created_list

def file_mime_type(file_path):
    mime_type = magic.from_file(file_path, mime=True)
    return mime_type

def create_post_folder(post_id):
    try:
        file_path = Path(f"posts/{post_id}")
        file_path.mkdir(exist_ok=False)
    except FileExistsError:
        return "alreadyexists"

def create_clips_folder(post_id):
    try:
        file_path = Path(f"posts/clips/{post_id}")
        file_path.mkdir(exist_ok=False)
    except FileExistsError:
        pass

def addposttl(post_id, privacy, user_id):
    with open("posts/total_post.json", 'r+') as post:
        data = json.load(post)
        try: 
            if post_id in data["posts"]["post"]:
                return "alreadyexists"
            if post_id in data["private_posts"]["post"]:
                return "alreadyexists"
        except IndexError:
            pass
        if privacy == "on":
            data["private_posts"]["post"].append([post_id, str(user_id)])
            post.seek(0)
            json.dump(data, post, sort_keys=True, indent=4)
            post.truncate()
        else:
            data["posts"]["post"].append(post_id)
            post.seek(0)
            json.dump(data, post, sort_keys=True, indent=4)
            post.truncate()
    
def addclipttl(post_id, privacy, user_id):
    with open("posts/clips/total_clips.json", 'r+') as post:
        data = json.load(post)
        try: 
            if post_id in data["clips"]["clip"]:
                return "alreadyexists"
            if post_id in data["clips"]["clip"]:
                return "alreadyexists"
        except IndexError:
            pass
        if privacy == "on":
            data["private_clips"]["clip"].append([post_id, str(user_id)])
            post.seek(0)
            json.dump(data, post, sort_keys=True, indent=4)
            post.truncate()
        else:
            data["clips"]["clip"].append(post_id)
            post.seek(0)
            json.dump(data, post, sort_keys=True, indent=4)
            post.truncate()

def create_post(post_info):
    with open(f'posts/{post_info["post_id"]}/post.json', 'w') as outfile:
        json.dump(post_info, outfile, sort_keys=True, indent=4)
    addposttl(post_info["post_id"], post_info["privacy"], post_info["user_id"])
    create_post_extras(post_info["post_id"])
    if post_info["clips"] == True:
        clips_list(post_info)
    return "completed"

def clips_list(post_info):
    create_clips_folder(post_info["post_id"])
    temp_data = create_clips_template(post_info)
    with open(f'posts/clips/{post_info["post_id"]}/clips.json', 'w') as file:
        json.dump(temp_data, file, sort_keys=True, indent=4)
    addclipttl(post_info["post_id"], post_info["privacy"], post_info["user_id"])
    change_clip_total_by_one()

def create_post_extras(post_id):
    comments = {
        "comments": [
            
        ]
    }
    with open(f'posts/{post_id}/comments.json', "w") as comment_file:
        json.dump(comments, comment_file, sort_keys=True, indent=4)
    likes = {
        "likes_total": 0,
        "likers": [
            
        ]
    }   
    with open(f'posts/{post_id}/likes.json', 'w') as likes_file:
        json.dump(likes, likes_file, sort_keys=True, indent=4)
        
def read_comments(post_id):
    with open(f'posts/{post_id}/comments.json', 'r') as comment_file:
        comments = json.load(comment_file)
        return comments

def read_likes(post_id):
    with open(f'posts/{post_id}/likes.json', 'r') as likes_file:
        likes = json.load(likes_file)
        return likes["likes_total"]
    
def add_like(post_id, user_id):
    with open(f'posts/{post_id}/likes.json', 'r+') as likes_file:
        likes_data = json.load(likes_file)
        if user_id in likes_data["likers"]:
            return "already_liked"
        else:
            likes_data["likes_total"] = int(likes_data["likes_total"]) + 1
            likes_data["likers"].append(user_id)
            likes_file.seek(0)
            json.dump(likes_data, likes_file, sort_keys=True, indent=4)
            likes_file.truncate()
        add2likelist(post_id)
    
def remove_like(post_id, user_id):
    with open(f'posts/{post_id}/likes.json', 'r+') as likes_file:
        likes_data = json.load(likes_file)
        if user_id not in likes_data["likers"]:
            return "not_liked"
        else:
            likes_data["likes_total"] = int(likes_data["likes_total"]) - 1
            likes_data["likers"].remove(user_id)
            likes_file.seek(0)
            json.dump(likes_data, likes_file, sort_keys=True, indent=4)
            likes_file.truncate()
            add2likelist(post_id)
            return "done"
    
def check_if_liked(post_id, user_id):
    with open(f'posts/{post_id}/likes.json', 'r') as likes_file:
        likes_data = json.load(likes_file)
        if user_id in likes_data["likers"]:
            return "liked"
        else:
            return "not_liked"

def add2likelist(post_id):
    with open(f'posts/total_likes.json', 'r+') as ltotal_file:
        likes_data = json.load(ltotal_file)
        post_info = [post_id, read_likes(post_id)]
        already_in_list = False
        for post in likes_data["liked_htl"]:
            if post_info[0] == post[0]:
                already_in_list = True
                items_index = likes_data["liked_htl"].index(post)
        if already_in_list == True:
            likes_data["liked_htl"].pop(items_index)
        add = False
        for post in likes_data["liked_htl"]:
            if add == True:
                break
            if int(post_info[1]) > int(post[1]):
                index = likes_data["liked_htl"].index(post)
                add = True
            elif int(post_info[1]) == int(post[1]):
                index = likes_data["liked_htl"].index(post)
                add = True
        if add == False:
            likes_data["liked_htl"].append(post_info)
        else:
            likes_data["liked_htl"].insert(index, post_info)
        ltotal_file.seek(0)
        json.dump(likes_data, ltotal_file, sort_keys=True, indent=4)
        ltotal_file.truncate()
    
def readlikelist(home_screen_post, friend_list_len):
    with open(f'posts/total_likes.json', 'r') as ltotal_file:
        to_be_used = []
        likes_data = json.load(ltotal_file)
        if int(home_screen_post)-friend_list_len > len(likes_data["liked_htl"]):
            for i in range(len(likes_data["liked_htl"])):
                to_be_used.append(likes_data["liked_htl"][i])
        else:
            for i in range(home_screen_post-friend_list_len):
                to_be_used.append(likes_data["liked_htl"][i])
        return to_be_used
        
def bookmark_post(post_id, user_id):
    with open(f'users/{user_id}.json', 'r+') as user_file:
        data = json.load(user_file)
        if post_id in data["saved_posts"]:
            return "already_saved"
        else:
            data["saved_posts"].append(post_id)
            user_file.seek(0)
            json.dump(data, user_file, sort_keys=True, indent=4)
            user_file.truncate()
    
def unbookmark_post(post_id, user_id):
    with open(f'users/{user_id}.json', 'r+') as user_file:
        data = json.load(user_file)
        if post_id not in data["saved_posts"]:
            return "not_saved"
        else:
            data["saved_posts"].remove(post_id)
            user_file.seek(0)
            json.dump(data, user_file, sort_keys=True, indent=4)
            user_file.truncate()
            
def check_if_bookmarked(post_id, user_id):
    with open(f'users/{user_id}.json', 'r') as user_file:
        user_data = json.load(user_file)
        if post_id in user_data["saved_posts"]:
            return "bookmarked"
        else:
            return "not_bookmarked"
    
def check_viewable(post_id, user_id):
    try:
        with open(f"posts/{post_id}/post.json", 'r') as post_file:
            file = json.load(post_file)
            if file["privacy"] == "on":
                poster_id = str(file["user_id"])
            else:
                return "readable"
    except FileNotFoundError:
        return "error"
    with open(f"users/{user_id}.json", 'r') as user_info:
        data = json.load(user_info)
        if poster_id in data["friends"]:
            return "readable"
        else:
            return "not_readable"
        
def check_viewable_w_agecheck(post_id, user_id, age):
    try:
        with open(f"posts/{post_id}/post.json", 'r') as post_file:
            file = json.load(post_file)
            if file["privacy"] == "on":
                poster_id = str(file["user_id"])
                if age == "16":
                    if file["age_rating"] != "16":
                        return "not_readable"
            else:
                if age == "16":
                    if file["age_rating"] == "16":
                        return "readable"
                    else:
                        return "not_readable"
                else:
                    return "readable"
    except FileNotFoundError:
        return "error"
    with open(f"users/{user_id}.json", 'r') as user_info:
        data = json.load(user_info)
        if poster_id in data["friends"]:
            return "readable"
        else:
            return "not_readable"
            
def add_comment(post_id, user_id, user_username, content):
    with open(f'posts/{post_id}/comments.json', 'r+') as comments_file:
        comment_data = json.load(comments_file)
        comment_add_data = {
            "content": content,
            "user": user_username,
            "user_id": user_id
        }
        comment_data["comments"].append(comment_add_data)
        comments_file.seek(0)
        json.dump(comment_data, comments_file, sort_keys=True, indent=4)
        comments_file.truncate()
    
def load_posts(home_screen_posts, friends_ids, user_age):
    with open("posts/total_post.json", 'r') as post:
        data = json.load(post)
    viewable_posts = []
    for friends in data["private_posts"]["post"]:
        print(friends)
        if friends[1] in friends_ids:
            if user_age != "18":
                if get_post_age(friends[0]) == "16":
                    viewable_posts.append(friends[0])
            else:
                viewable_posts.append(friends[0])
    for pub_data in data["posts"]["post"]:
        if user_age != "18":
            if get_post_age(pub_data) == "16":
                viewable_posts.append(pub_data)
        else:
            viewable_posts.append(pub_data)
    if int(home_screen_posts) > len(viewable_posts):
        nums_to_be_used = []
        for _ in viewable_posts:
            a_post = random.randint(0, int(len(viewable_posts)) - 1)
            while a_post in nums_to_be_used:
                a_post = random.randint(0, int(len(viewable_posts)) - 1)
                if a_post not in nums_to_be_used:
                    break
            nums_to_be_used.append(a_post)
        posts_to_be_used = []
        for numbers in nums_to_be_used:
            posts_to_be_used.append(viewable_posts[numbers])
    else:
        nums_to_be_used = []
        for _ in range(home_screen_posts):
            a_post = random.randint(1, int(len(viewable_posts)))
            while a_post in nums_to_be_used:
                a_post = random.randint(1, int(len(viewable_posts)))
                if a_post not in nums_to_be_used:
                    break
            nums_to_be_used.append(a_post)
        posts_to_be_used = []
        for numbers in nums_to_be_used:
            posts_to_be_used.append(viewable_posts[numbers - 1])
    return posts_to_be_used

def load_clips(home_screen_posts, friends_ids, user_age):
    with open("posts/clips/total_clips.json", 'r') as post:
        data = json.load(post)
    viewable_clips = []
    for friends in data["private_clips"]["clip"]:
        if friends[1] in friends_ids:
            if user_age != "18":
                if get_post_age(friends) == "16":
                    viewable_clips.append(friends[0])
            else:
                viewable_clips.append(friends[0])
    for pub_data in data["clips"]["clip"]:
        if user_age != "18":
            if get_post_age(pub_data) == "16":
                viewable_clips.append(pub_data)
        else:
            viewable_clips.append(pub_data)
    if int(home_screen_posts) > len(viewable_clips):
        nums_to_be_used = []
        for _ in viewable_clips:
            a_clip = random.randint(0, int(len(viewable_clips)) - 1)
            while a_clip in nums_to_be_used:
                a_clip = random.randint(0, int(len(viewable_clips)) - 1)
                if a_clip not in nums_to_be_used:
                    break
            nums_to_be_used.append(a_clip)
        clips_to_be_used = []
        for numbers in nums_to_be_used:
            clips_to_be_used.append(viewable_clips[numbers])
    else:
        nums_to_be_used = []
        for _ in range(home_screen_posts):
            a_post = random.randint(1, int(len(viewable_clips)) - 1)
            while a_post in nums_to_be_used:
                a_post = random.randint(1, int(len(viewable_clips)) - 1)
                if a_post not in nums_to_be_used:
                    break
            nums_to_be_used.append(a_post)
        clips_to_be_used = []
        for numbers in nums_to_be_used:
            clips_to_be_used.append(viewable_clips[numbers - 1])
    return clips_to_be_used

def load_trending(home_screen_posts, user_id, user_age):
    friends = read_friends(user_id)
    if friends != []:
        friends_post = load_friends_post(friends)
    else:
        friends_post = []
    post_list = readlikelist(home_screen_posts, len(friends_post))
    final_post_list = load_post_with_friends(friends_post, post_list, user_age)
    return final_post_list
    
def load_post_with_friends(friends_posts, post_list, user_age):
    temp_friends_posts = []
    for post in friends_posts:
        if user_age != "18":
            if get_post_age(post) == "16":
                likes = read_likes(post)
                temp_friend_post = [post, likes]
                temp_friends_posts.append(temp_friend_post)
        else:
            likes = read_likes(post)
            temp_friend_post = [post, likes]
            temp_friends_posts.append(temp_friend_post)
    temp_post_list = []
    for post in post_list:
        print(post)
        print(post_list)
        if user_age != "18":
            if get_post_age(post[0]) == "16":
                temp_post_list.append(post)
        else:
            temp_post_list.append(post)
    for friend_post_id in temp_friends_posts:
        added = False
        for post in temp_post_list:
            if int(friend_post_id[1]) > int(post[1]) or int(friend_post_id[1]) == int(post[1]):
                index = temp_post_list.index(post)
                temp_post_list.insert(index, friend_post_id)
                added = True
                break
        if added != True:
            temp_post_list.append(friend_post_id)
    final_post_list = []
    for post in temp_post_list:
        final_post_list.append(post[0])
    return final_post_list

def load_friends_post(friend_list):
    with open("posts/total_post.json", 'r') as post:
        data = json.load(post)
    posts = []
    for friends in data["private_posts"]["post"]:
        if friends[1] in friend_list:
            posts.append(friends[0])
    print(posts)
    return posts

def check_user_age(user_id):
    with open(f"users/{user_id}.json", 'r') as user_data:
        data = json.load(user_data)
        return data["age"]
    
def read_posts(post_id):
    try:
        with open(f"posts/{post_id}/post.json", 'r') as post_json:
            data = json.load(post_json)
            return data
    except FileNotFoundError:
        return "error"
    
def read_clips(post_id):
    try:
        with open(f"posts/clips/{post_id}/clips.json", 'r') as post_json:
            data = json.load(post_json)
            return data
    except FileNotFoundError:
        return "error"
    
def read_user(user_id):
    with open(f'users/{user_id}.json', 'r') as user_json:
        user_data = json.load(user_json)
        return user_data
    
def change_description(user_id, description):
    with open(f'users/{user_id}.json', 'r+') as user_json:
        data = json.load(user_json)
        data["description"] = description
        user_json.seek(0)
        json.dump(data, user_json, sort_keys=True, indent=4)
        user_json.truncate()
        
def custom_pfp_data(user_id, file_type):
    with open(f'users/{user_id}.json', 'r+') as user_json:
        data = json.load(user_json)
        data["custom_pfp"] = True
        data["pfp_type"] = file_type
        user_json.seek(0)
        json.dump(data, user_json, sort_keys=True, indent=4)
        user_json.truncate()

def check_if_user_exists(user_id):
    try:
        with open(f'users/{user_id}.json', 'r') as user:
            return "exists"
    except FileNotFoundError:
        return "none"
    
def modify_for_clips_only(post_id):
    clips = read_posts(post_id)
    to_be_used = []
    for item in clips["images"]:
        if '.mp4' in item:
            to_be_used.append(item)
    return to_be_used

def read_total(post_id):
    clips = read_posts(post_id)
    return clips["total_images"]

def get_post_name(post_id):
    with open(f'posts/{post_id}/post.json', 'r') as data:
        post_data = json.load(data)
        return post_data["title"]
    
def get_usrname_by_postid(post_id):
    with open(f'posts/{post_id}/post.json', 'r') as data:
        post_data = json.load(data)
        return [post_data["user"], post_data["user_id"]]
    
def get_bookmarked_posts(user_id):
    with open(f'users/{user_id}.json', 'r') as user_file:
        user_info = json.load(user_file)
        posts = user_info["saved_posts"]
    bookmarked_post = []
    for post in posts:
        post_name = get_post_name(post)
        bookmarked_post.append([post, post_name])
    return bookmarked_post

def add_user_profile_info(post_id):
    user_id = get_usrname_by_postid(post_id)[1]
    with open(f'users/{user_id}.json', 'r') as user_file:
        user_info = json.load(user_file)
        custom_pfp = user_info["custom_pfp"]
        pfp_type = user_info["pfp_type"]
        return [custom_pfp, f"pfp/{user_id}{pfp_type}"]
    
def get_post_age(post_id):
    with open(f'posts/{post_id}/post.json', 'r') as data:
        post_data = json.load(data)
        return post_data["age_rating"]