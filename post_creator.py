#!/usr/bin/env python3
import json, pyclamd, magic, random
from pathlib import Path

def total_posts():
    with open('posts/total_post.txt', 'r') as post:
        return post.read()

def change_post_total_by_one():
    with open('posts/total_post.txt', 'r') as post:
        total = int(post.read())
        
    with open('posts/total_post.txt', 'w') as post:
        total += 1
        post.write(str(total))
        
def change_post_total_by_minus_one():
    with open('posts/total_post.txt', 'r') as post:
        total = int(post.read())
        print(total)
        print(type(total))
        
    with open('posts/total_post.txt', 'w') as post:
        total -= 1
        post.write(str(total))
        
def change_private_total_by_one():
    with open('posts/total_post.txt', 'r') as post:
        total = int(post.read())
        
    with open('posts/total_post.txt', 'w') as post:
        total += 1
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
    
def create_list(id, title, desc, user, userid, likes, privacy, images, total_images, age_rating):
    created_list = {
        "post_id": id,
        "title": title,
        "description": desc,
        "user": user,
        "user_id": userid,
        "likes": likes,
        "privacy": privacy,
        "images": images,
        "total_images": total_images,
        "age_rating": age_rating
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

def addposttl(post_id, privacy):
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
            data["private_posts"]["post"].append(post_id)
            post.seek(0)
            json.dump(data, post, sort_keys=True, indent=4)
            post.truncate()
        else:
            data["posts"]["post"].append(post_id)
            post.seek(0)
            json.dump(data, post, sort_keys=True, indent=4)
            post.truncate()

def create_post(post_info):
    with open(f'posts/{post_info["post_id"]}/post.json', 'w') as outfile:
        json.dump(post_info, outfile, sort_keys=True, indent=4)
    addposttl(post_info["post_id"], post_info["privacy"])
    return "completed"

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
            a_post = random.randint(1, int(len(viewable_posts)) - 1)
            while a_post in nums_to_be_used:
                a_post = random.randint(1, int(len(viewable_posts)) - 1)
                if a_post not in nums_to_be_used:
                    break
            nums_to_be_used.append(a_post)
        posts_to_be_used = []
        for numbers in nums_to_be_used:
            posts_to_be_used.append(viewable_posts[numbers - 1])
    return posts_to_be_used

def read_posts(post_id):
    print(post_id)
    with open(f"posts/{post_id}/post.json", 'r') as post_json:
        data = json.load(post_json)
        return data