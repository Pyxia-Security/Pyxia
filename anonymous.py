import json, random
from search_system import read_posts_search, add_usrnm_and_pstnm

def anonymous_load_posts():
    home_screen_posts = 10
    with open("posts/total_post.json", 'r') as post:
        data = json.load(post)
    viewable_posts = []
    for pub_data in data["posts"]["post"]:
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

def anonymous_load_clips():
    home_screen_posts = 10
    with open("posts/clips/total_clips.json", 'r') as post:
        data = json.load(post)
    viewable_clips = []
    for pub_data in data["clips"]["clip"]:
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

def anonymous_load_trending():
    home_screen_posts = 10
    post_list = anonymous_readlikelist(home_screen_posts)
    return post_list

def anonymous_readlikelist(home_screen_post):
    with open(f'posts/total_likes.json', 'r') as ltotal_file:
        to_be_used = []
        likes_data = json.load(ltotal_file)
        if int(home_screen_post) > len(likes_data["liked_htl"]):
            for i in range(len(likes_data["liked_htl"])):
                to_be_used.append(likes_data["liked_htl"][i][0])
        else:
            for i in range(home_screen_post):
                to_be_used.append(likes_data["liked_htl"][i][0])
        return to_be_used
    
def anonymous_check_viewable(post_id):
    try:
        with open(f"posts/{post_id}/post.json", 'r') as post_file:
            file = json.load(post_file)
            if file["privacy"] == "on":
                return "not_readable"
            else:
                return "readable"
    except FileNotFoundError:
        return "error"
    
def anonymous_search_for(params):
    post_data = anonymous_get_post_data4srch()
    posts = read_posts_search(post_data, params)
    final_post_data = add_usrnm_and_pstnm(posts)
    return final_post_data

def anonymous_get_post_data4srch():
    with open('posts/total_post.json', 'r') as posts:
        post_data = json.load(posts)
        public_posts = post_data["posts"]["post"]
    return public_posts