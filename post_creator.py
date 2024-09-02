#!/usr/bin/env python3
import json, os, pyclamd, magic
from pathlib import Path

def total_posts():
    with open('posts/total_post.txt', 'r') as post:
        return post.read()

def change_post_total_by_one():
    with open('posts/total_post.txt', 'r') as post:
        total = int(post.read())
        print(total)
        print(type(total))
        
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

temp_post_info = {
    "post_id": total_posts(),
    "title": "Test Post",
    "description": "This is a test post",
    "date": "20-08-2024/6:12",
    "user": "Seb",
    "user_id": "1",
    "likes": "0",
    "privacy": "public",
    "images": ['img1.jpg', 'img2.jpg'],
    "age_rating": "16"
}

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
    return (created_list)

def file_mime_type(file_path):
    mime_type = magic.from_file(file_path, mime=True)
    return mime_type

def create_post_folder(post_id):
    try:
        file_path = Path(f"posts/{post_id}")
        file_path.mkdir(exist_ok=False)
    except FileExistsError:
        return ('alreadyexists')

def create_post(post_info):
    with open(f'posts/{post_info["post_id"]}/post.json', 'w') as outfile:
        json.dump(post_info, outfile, sort_keys=True, indent=4)
    return "completed"
    
#create_post(temp_post_info)