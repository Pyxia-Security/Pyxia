#!/usr/bin/env python3
import json, pyclamd, magic, random
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
            return "done"
    
def check_if_liked(post_id, user_id):
    with open(f'posts/{post_id}/likes.json', 'r') as likes_file:
        likes_data = json.load(likes_file)
        if user_id in likes_data["likers"]:
            return "liked"
        else:
            return "not_liked"

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
    
def load_posts(home_screen_posts, friends_ids):
    with open("posts/total_post.json", 'r') as post:
        data = json.load(post)
    viewable_posts = []
    for friends in data["private_posts"]["post"]:
        if friends[1] in friends_ids:
            viewable_posts.append(friends[0])
    for pub_data in data["posts"]["post"]:
        viewable_posts.append(pub_data)
    if home_screen_posts > len(viewable_posts):
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

def load_clips(home_screen_posts, friends_ids):
    with open("posts/clips/total_clips.json", 'r') as post:
        data = json.load(post)
    viewable_clips = []
    for friends in data["private_clips"]["clip"]:
        if friends[1] in friends_ids:
            viewable_clips.append(friends[0])
    for pub_data in data["clips"]["clip"]:
        viewable_clips.append(pub_data)
    if home_screen_posts > len(viewable_clips):
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