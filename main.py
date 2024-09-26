#!/usr/bin/env python3
#Programmed and Developed by @OfficialJavaScript of Pyxia Security.
from flask import Flask, render_template, redirect, request, session, abort, url_for
import os, flask_login, shutil, json, datetime
from flask_login import current_user
from database import db, Mapped, mapped_column
from decouple import config
from lib.flask_recaptcha import ReCaptcha
import argon2
from pathlib import Path
from post_creator import *
from chat_creator import *
from friend_system import *
from user_agents import parse

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{config("NAME")}:{config("PASSWORD")}@localhost:{config("PORT")}/{config("DATABASE")}"
app.config["RECAPTCHA_SECRET_KEY"] = config("RECAPTCHA_SECRET_KEY")
app.config["RECAPTCHA_SITE_KEY"] = config("RECAPTCHA_SITE_KEY")
app.config["RECAPTCHA_ENABLED"] = config("RECAPTCHA_ENABLED")
app.config['UPLOAD_FOLDER'] = "C:\\Digi Project - Social Media\\Pyxia\\posts\\"
app.config['PFPUPLOAD_FOLDER'] = "C:\\Digi Project - Social Media\\Pyxia\\static\\pfp\\"
recaptcha = ReCaptcha(app=app)
db.init_app(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
home_screen_posts = 10
phash = argon2.PasswordHasher()

class User(db.Model, flask_login.UserMixin):
    __tablename__ = "userdb"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str]
    age: Mapped[int]

@login_manager.user_loader
def user_loader(user_id):
    user = db.get_or_404(User, int(user_id))
    return user

@app.route("/", methods=['GET'])
def index():
    session['error'] = False
    session['already_exists'] = False
    session['robot'] = False
    get_user_agent()
    #Note to self: Personal user id is added to the friends list so they can see their own posts, so remove when checking for friends in list (do something like friends[1] onwards, skipping friends[0] which = user_id).
    return render_template("main.html", yes=session["device_type"])

@app.route("/notifications", methods=['GET'])
def notifications_page():
    return render_template("notifications.html")

@app.route("/pyxia", methods=['GET'])
def home():
    session['error'] = False
    session['already_exists'] = False
    session['robot'] = False
    if current_user.is_authenticated == False:
            return redirect('/')
    posts_list = load_posts(home_screen_posts, read_friends(current_user.id))
    post_info = {
        "posts": [
            
        ]
    }
    for post in posts_list:
        info = read_posts(post)
        likes = read_likes(info["post_id"])
        info["likes"] = likes
        liked = check_if_liked(info["post_id"], current_user.id)
        info["liked"] = liked
        bookmarked = check_if_bookmarked(int(info["post_id"]), current_user.id)
        info["bookmarked"] = bookmarked
        post_info["posts"].append(info)
    return render_template("index.html", posts=post_info)
        
@app.route('/pyxia/posts/<id>', methods=['GET'])
def posts_page(id):
    if current_user.is_authenticated == False:
        return redirect('/')
    try:
        post_id = int(id)
    except ValueError:
        return abort(404)
    response = check_viewable(post_id, current_user.id)
    if response == "error":
        return abort(404)
    elif response == "not_readable":
        return abort(403)
    elif response == "readable":
        data = read_posts(post_id)
        if data == "error":
            return abort(404)
        likes = read_likes(id)
        data["likes"] = likes
        liked = check_if_liked(post_id, current_user.id)
        data["liked"] = liked
        bookmarked = check_if_bookmarked(post_id, current_user.id)
        data["bookmarked"] = bookmarked
        comments = read_comments(post_id)
        return render_template("posts.html", post=data, comments=comments["comments"])
    else:
        return abort(403)
     
@app.route('/pyxia/like_post/<id>', methods=['POST'])
def like_post(id):
    if current_user.is_authenticated == False:
        return redirect('/')
    try:
        post_to_be_liked = int(id)
    except ValueError:
        return "", 403
    response = check_viewable(post_to_be_liked, current_user.id)
    if response == "error":
        return "", 403
    elif response == "not_readable":
        return "", 403
    add_like(post_to_be_liked, current_user.id)
    likes = read_likes(post_to_be_liked)
    return str(likes), 201

@app.route('/pyxia/unlike_post/<id>', methods=['POST'])
def unlike_post(id):
    if current_user.is_authenticated == False:
        return redirect('/')
    try:
        post_to_be_unliked = int(id)
    except ValueError:
        return "", 403
    response = check_viewable(post_to_be_unliked, current_user.id)
    if response == "error":
        return "", 403
    elif response == "not_readable":
        return "", 403
    remove_response = remove_like(post_to_be_unliked, current_user.id)
    if remove_response == "not_liked":
        return "", 403
    likes = read_likes(post_to_be_unliked)
    return str(likes), 201
        
@app.route('/pyxia/save_post/<id>', methods=['POST'])
def save_post(id):
    if current_user.is_authenticated == False:
        return redirect('/')
    try:
        post_to_be_saved = int(id)
    except ValueError:
        return "", 403
    response = check_viewable(post_to_be_saved, current_user.id)
    if response == "error":
        return "", 403
    elif response == "not_readable":
        return "", 403
    bookmark_response = bookmark_post(post_to_be_saved, current_user.id)
    if bookmark_response == "already_saved":
        return  "", 403
    return "", 201
   
@app.route('/pyxia/unsave_post/<id>', methods=['POST'])
def unsave_post(id):
    if current_user.is_authenticated == False:
        return redirect('/')
    try:
        post_to_be_saved = int(id)
    except ValueError:
        return "", 403
    response = check_viewable(post_to_be_saved, current_user.id)
    if response == "error":
        return "", 403
    elif response == "not_readable":
        return "", 403
    bookmark_response = unbookmark_post(post_to_be_saved, current_user.id)
    if bookmark_response == "not_saved":
        return  "", 403
    return "", 201
   
@app.route('/pyxia/add_comment/<id>', methods=['POST'])
def add_comment_page(id):
    if current_user.is_authenticated == False:
        return redirect('/')
    try:
        post_id = int(id)
    except ValueError:
        return abort(404)
    response = check_viewable(post_id, current_user.id)
    if response == "error":
        return abort(403)
    elif response == "not_readable":
        return abort(403)
    comment = request.form.get('comment')
    if len(comment) > 301:
        return abort(405, "Content larger than 300")
    add_comment(post_id, current_user.id, current_user.username, request.form.get('comment'))
    return redirect(f'/pyxia/posts/{post_id}')
   
@app.route('/pyxia/update_description', methods=['POST'])
def description():
    if current_user.is_authenticated == False:
        return redirect('/')
    change_description(current_user.id, request.form.get('description'))
    return redirect('/pyxia/profile')

@app.route('/pyxia/profile/change_pfp', methods=['GET'])
def change_pfp():
    if current_user.is_authenticated == False:
        return redirect('/')
    if request.method == "GET":
        return render_template("change_pfp.html")
    
@app.route('/pyxia/profile/change_pfp_post', methods=['POST'])
def change_pfp_post():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        mimes = ['image/jpeg', 'image/jpg', 'image/png']
        if uploaded_file.filename.lower().endswith('.png'):
            file_type = ".png"
        elif uploaded_file.filename.lower().endswith(('.jpg')):
            file_type = ".jpg"
        elif uploaded_file.filename.lower().endswith(('.jpeg')):
            file_type = ".jpeg"
        else:
            return redirect('/pyxia/profile/change_pfp')
        uploaded_file.save(os.path.join(app.config["PFPUPLOAD_FOLDER"], f"{current_user.id}{file_type}"))
        custom_pfp_data(current_user.id, file_type)
        scan_result = scan_upload(os.path.join(app.config["PFPUPLOAD_FOLDER"], f"{current_user.id}{file_type}"))
        if scan_result == "malware":
            post_path = Path(f"users/pfp/{current_user.id}.{file_type}")
            os.remove(post_path)
            return redirect('/pyxia/profile/change_pfp')
        mime = file_mime_type(os.path.join(app.config["PFPUPLOAD_FOLDER"], f"{current_user.id}{file_type}"))
        if mime not in mimes:
            post_path = Path(f"users/pfp/{current_user.id}.{file_type}")
            os.remove(post_path)
            return redirect('/pyxia/profile/change_pfp')
    return redirect('/pyxia/profile')

@app.route('/pyxia/profile/<user_id>', methods=['GET'])
def user_profile(user_id):
    if current_user.is_authenticated == False:
        return redirect('/')
    try:
        clear_user_id = int(user_id)
    except ValueError:
        return abort(404)
    if str(user_id) == str(current_user.id):
        return redirect("/pyxia/profile")
    exists = check_if_user_exists(clear_user_id)
    if exists == "none":
        return abort(404)
    friend_check = check_if_friends(current_user.id, clear_user_id)
    if friend_check == True:
        friend = True
    else:
        friend = False
    user_data = get_user_profile(clear_user_id)
    return render_template("profile.html", user=user_data, friend=friend)
   
@app.route('/filething', methods=['POST'])
def file_thing():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return redirect('/')
   
def get_user_agent():
    if "user_agent" in session:
        if session["user_agent"] != "":
            return session["user_agent"]
    user_agent = request.headers.get('User-Agent')
    user_agent_parsed = parse(user_agent)
    session["device_type"] = ("mobile" if user_agent_parsed.is_mobile else "desktop")

@app.route("/test_mobile_and_pc")
def tester_site():
    return render_template("tester2.html")

@app.route("/a")
def anonymous():
    if current_user.is_authenticated == True:
        return redirect('/')
    return render_template("anonymous.html")

def get_user(username):
    return db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()

def check_user(username):
    return db.session.query(db.exists().where(User.username==username)).scalar()

def check_email(email):
    return db.session.query(db.exists().where(User.email==email)).scalar()
    
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if current_user.is_authenticated == True:
            return redirect('/')
        if 'robot' in session:
            if session['robot'] == True:
                return render_template("login.html", error=False, robot=True)
        if 'error' in session:
            if session['error'] == "True" or session['error'] == True:
                return render_template("login.html", error=True, robot=True)
        return render_template("login.html", error=False, robot=False)
    else:
        if recaptcha.verify():
            username = request.form.get('username')
            try:
                user = get_user(username)
                if user == None or user == "None":
                    session['error'] = True
                    session['robot'] = False
                    return redirect('/login')
                try:
                    hash_verify = phash.verify(user.password, request.form.get('password'))
                    if hash_verify == True:
                        flask_login.login_user(user)
                        session['error'] = "False"
                        session['robot'] = False
                        set_login_time(current_user.id, False)
                        return redirect('/pyxia')
                    else:
                        session['error'] = True
                        return redirect('/login')
                except argon2.exceptions.VerifyMismatchError:
                    session['error'] = True
                    return redirect('/login')
                    
            except Exception as e:
                print(e)
                abort(500)
        else:
            session['robot'] = True
            return redirect('/login')
            
@app.route('/logout')
def logout():
    if current_user.is_authenticated == False:
        return redirect('/')
    session['error'] = False
    session['already_exists'] = False
    session['robot'] = False
    set_login_time(current_user.id, True)
    flask_login.logout_user()
    return redirect('/')

@app.route('/signup-ert')
def signup_ert():
    session['error'] = False
    session['already_exists'] = False
    session['robot'] = False
    return redirect('/signup')

@app.route('/login-ert')
def login_ert():
    session['error'] = False
    session['already_exists'] = False
    session['robot'] = False
    return redirect('/login')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        if current_user.is_authenticated == True:
                return redirect('/') 
        if 'error' in session:
            if session['error'] == True:
                return render_template("signup.html", error=True, already_exists=False)
        if 'already_exists' in session:
            if session['already_exists'] == True:
                return render_template("signup.html", error=False, already_exists=True)
        return render_template("signup.html", error=False, already_exists=False)
    else:
        if recaptcha.verify():
            ages = ['16', '18']
            email = request.form.get('email')
            username = request.form.get('username')
            age = request.form.get('age')
            if age not in ages:
                return redirect('signup')
            chkemail = check_email(email)
            if chkemail == True or chkemail == "True":
                session['already_exists'] = True
                return redirect('/signup')
            chkusr = check_user(username)
            if chkusr == True or chkusr == "True":
                session['already_exists'] = True
                return redirect('/signup')
            password = request.form.get('password')
            conf_password = request.form.get('confirm-password')
            if password != conf_password:
                session['error'] = True
                conf_password = ""
                password = ""
                return redirect('/signup')
            else:
                password = phash.hash(request.form.get('password'))
                conf_password = ""
                session['error'] = False
                session['already_exists'] = False
                session['robot'] = False
                user = User(
                    email=email,
                    username=username,
                    password=password,
                    age=age
                )
                db.session.add(user)
                db.session.commit()
                user_for_login = get_user(username)
                flask_login.login_user(user_for_login)
                create_user_file(current_user.id, username, age)
                set_login_time(current_user.id, False)
                return redirect('/pyxia')
        else:
            session['robot'] = True
            redirect('/signup')

@app.route('/pyxia/profile', methods=['GET'])
def profile_page():
    if current_user.is_authenticated == False:
        return redirect('/') 
    user_data = read_user(current_user.id)
    if user_data["custom_pfp"] == True:
        image_data = get_image(user_data)
    else:
        image_data = None
    return render_template("myprofile.html", user=user_data, pfp=image_data)

@app.route('/pyxia/search', methods=['GET'])
def search():
    if current_user.is_authenticated == False:
        return redirect('/')
    return render_template("search.html")

@app.route('/pyxia/friends', methods=['GET'])
def friends():
    if current_user.is_authenticated == False:
        return redirect('/')
    friends = set_user_names(current_user.id)
    return render_template("friends.html", friends=friends)

@app.route('/pyxia/trending', methods=['GET'])
def trending():
    if current_user.is_authenticated == False:
        return redirect('/')
    return render_template("trending.html")

@app.route('/pyxia/clips', methods=['GET'])
def clips():
    if current_user.is_authenticated == False:
        return redirect('/')
    clips_list = load_clips(home_screen_posts, read_friends(current_user.id))
    clips_info = {
        "clips": [
            
        ]
    }
    for clip in clips_list:
        info = read_clips(clip)
        likes = read_likes(info["post_id"])
        info["likes"] = likes
        liked = check_if_liked(info["post_id"], current_user.id)
        info["liked"] = liked
        bookmarked = check_if_bookmarked(int(info["post_id"]), current_user.id)
        info["bookmarked"] = bookmarked
        clips_info["clips"].append(info)
    return render_template("clips.html", clips=clips_info)

@app.route('/pyxia/create_post_proute', methods=['POST'])
def create_post_backend():
    files = request.files.getlist("file")
    post_id = total_posts()
    create_post_folder(post_id)
    change_post_total_by_one()
    if str(files) == str("[<FileStorage: '' ('application/octet-stream')>]") or files == "":
        images = 0
        temp_list = create_list(post_id, request.form.get("title"), request.form.get("description"), current_user.username, current_user.id, request.form.get("private"), None, images, request.form.get('age_rating'), False, [])
    else:
        images = len(files)
        file_list = []
        clips_list = []
        clips = False
        mimes = ['image/jpeg', 'image/jpg', 'image/png', 'video/mp4']
        time_through = 0
        for file in files:
            if file.filename.lower().endswith('.png'):
                file_type = ".png"
            elif file.filename.lower().endswith(('.jpg')):
                file_type = ".jpg"
            elif file.filename.lower().endswith(('.jpeg')):
                file_type = ".jpeg"
            elif file.filename.lower().endswith(('.mp4')):
                file_type = ".mp4"
                clips = True
                clips_list.append(str(os.path.join(app.config["UPLOAD_FOLDER"], f"{post_id}", f"post{time_through}{file_type}")))
            else:
                post_path = Path(f"posts/{post_id}")
                shutil.rmtree(post_path)
                change_post_total_by_minus_one()
                return('error')
            time_through += 1
            file_list.append(os.path.join(app.config["UPLOAD_FOLDER"], f"{post_id}", f"post{time_through}{file_type}"))
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], f"{post_id}", f"post{time_through}{file_type}"))
            mime = file_mime_type(os.path.join(app.config["UPLOAD_FOLDER"], f"{post_id}", f"post{time_through}{file_type}"))
            if mime not in mimes:
                post_path = Path(f"posts/{post_id}")
                shutil.rmtree(post_path)
                change_post_total_by_minus_one()
                return('error')
            scan_result = scan_upload(os.path.join(app.config["UPLOAD_FOLDER"], f"{post_id}", f"post{time_through}{file_type}"))
            if scan_result == "malware":
                post_path = Path(f"posts/{post_id}")
                shutil.rmtree(post_path)
                change_post_total_by_minus_one()
                return('error')
        temp_list = create_list(post_id, request.form.get("title"), request.form.get("description"), current_user.username, current_user.id, request.form.get("private"), file_list, images, request.form.get('age_rating'), clips, clips_list)
    response = create_post(temp_list)
    if response == "completed":
        return redirect('/pyxia')
    else:
        return('error')
    
@app.route('/pyxia/create_post', methods=['GET'])
def create_post_page():
    if current_user.is_authenticated == False:
        return redirect('/')
    return render_template("create_post.html")
    
def check_if_exists(id):
    file = Path(f"users/{id}.json")
    if file.is_file():
        return "yes"

def create_user_file(user_id, username, age):
    data = {
        "age": age,
        "chat_rooms": [],
        "conversation_with": [],
        "custom_pfp": False,
        "pfp_type": False,
        "username": username,
        "user_id": user_id,
        "friends": [
            f"{user_id}"
        ],
        "login_date": None,
        "logoff_time": 1,
        "saved_posts": [
            
        ],
        "description": f"Hello World! Welcome to {username}'s Pyxia page!",
        "settings": [
            
        ]
    }
    with open(f'users/{user_id}.json', 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4)
    
def get_image(user_data):
    data = url_for('static', filename=f'pfp/{ user_data["user_id"]}{ user_data["pfp_type"] }')
    return data

@app.route("/pyxia/chat", methods=['GET'])
def chat():
    if current_user.is_authenticated == False:
        return redirect('/')
    chats = read_user_chats(current_user.id)
    return render_template("chathome.html", chats=chats)

@app.route("/pyxia/chat/<chat_id>", methods=['GET'])
def chat_viewer(chat_id):
    if current_user.is_authenticated == False:
        return redirect('/')
    try:
        id_for_chat = int(chat_id)
    except ValueError:
        return abort(404)
    exist = check_if_exists_chat(id_for_chat)
    if exist != "exists":
        return abort(404)
    canread = check_if_user_can_read(current_user.id, id_for_chat)
    if canread != "can_read":
        return abort(401)
    chat_name = get_chat_name(id_for_chat)
    return render_template("chatroom.html", chat_id=id_for_chat, chat_name=chat_name[0])

@app.route("/pyxia/get_chat/<chat_id>")
def get_chat(chat_id):
    if current_user.is_authenticated == False:
        return redirect('/')
    try:
        id_for_chat = int(chat_id)
    except ValueError:
        return abort(404)
    exist = check_if_exists_chat(id_for_chat)
    if exist != "exists":
        return abort(404)
    canread = check_if_user_can_read(current_user.id, id_for_chat)
    if canread != "can_read":
        return abort(401)
    messages = read_messages(id_for_chat)
    return render_template("chatroom_chat.html", messages=messages)

@app.route('/pyxia/send_message/<chat_id>', methods=['POST'])
def send_message(chat_id):
    if current_user.is_authenticated == False:
        return "", 403
    try:
        id_for_chat = int(chat_id)
    except ValueError:
        return "", 404
    exist = check_if_exists_chat(id_for_chat)
    if exist != "exists":
        return "", 404
    canread = check_if_user_can_read(current_user.id, id_for_chat)
    if canread != "can_read":
        return "", 401
    message = request.form.get("message")
    if int(len(message)) > 301:
        return "Message too long", 404
    add_message(id_for_chat, current_user.id, current_user.username, message)
    return "", 200

@app.route('/pyxia/chat/create_room/<user_id>', methods=['GET'])
def create_room(user_id):
    if current_user.is_authenticated == False:
        return redirect('/')
    try:
        int_user_id = int(user_id)
    except ValueError:
        return abort(404)
    exists = check_if_user_exists(int_user_id)
    if exists == "none":
        return abort(404)
    conversation = check_user_conversation_list(current_user.id, int_user_id)
    if conversation == "already_exists":
        return redirect("/pyxia/chat")
    friend_check = check_if_friends(current_user.id, int_user_id)
    if friend_check == False:
        return abort(401)
    other_user_name = get_user_name(user_id)
    chat_name = f"{current_user.username} and {other_user_name}"
    create_chat_room(current_user.id, int_user_id, chat_name)
    add_user_conversation_to_user_list(current_user.id, int_user_id)
    return redirect("/pyxia/chat")

@app.route('/pyxia/check_auth', methods=['POST'])
def check_auth_time():
    if current_user.is_authenticated == False:
        return "", 401
    time = get_login_time(current_user.id)
    user_time = get_user_defined_time(current_user.id)
    if user_time == None:
        return "DISABLE", 200
    current_time = datetime.datetime.now()
    data = current_time-time
    if data > datetime.timedelta(hours=int(user_time)):
        return "redirect", 307
    else:
        return "OK", 200
    
def get_login_time(user_id):
    with open(f'users/{user_id}.json', 'r+') as user:
        user_data = json.load(user)
        login_time = user_data["login_date"]
        login_time_deltaformat = datetime.datetime.strptime(login_time, '%Y-%m-%d %H:%M:%S')
        return login_time_deltaformat

def set_login_time(user_id, is_logoff):
    if is_logoff == True:
        current_time = None
    else:
        current_time = str(datetime.datetime.now().replace(microsecond=0, second=0))
    with open(f'users/{user_id}.json', 'r+') as user_file:
        user_data = json.load(user_file)
        user_data["login_date"] = current_time
        user_file.seek(0)
        json.dump(user_data, user_file, sort_keys=True, indent=4)
        user_file.truncate()

def get_user_defined_time(user_id):
    with open(f'users/{user_id}.json', 'r+') as user:
        user_data = json.load(user)
        return user_data["logoff_time"]
    
def change_user_defined_time(user_id, time):
    times = [1, 2, 3, 4, 5, None]
    if time not in times:
        return abort(406)
    with open(f'users/{user_id}.json', 'r+') as user:
        user_data = json.load(user)
        user_data["logoff_time"] = time
        user.seek(0)
        json.dump(user_data, user, sort_keys=True, indent=4)
        user.trucate()

@login_manager.unauthorized_handler
def login_unauthorized_handler():
    return render_template("error/401.html"), 401

@app.errorhandler(401)
def unauthorized_handler(e):
    return render_template("error/401.html"), 401

@app.errorhandler(403)
def forbidden_handler(e):
    return render_template("error/403.html"), 403

@app.errorhandler(404)
def notfound_handler(e):
    return render_template("error/404.html"), 404

@app.errorhandler(410)
def gone_handler(e):
    return render_template("error/410.html"), 410

@app.errorhandler(500)
def intserverror_handler(e):
    return render_template("error/500.html"), 500

#@app.errorhandler(Exception)
#def unauthorized_handler(e):
    #return render_template("error/418.html", error=e), 418

@app.route("/teapot")
def teapoteasteregg():
    abort(405)

if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    # deepcode ignore RunWithDebugTrue: disable debug in final version, as is currently used for testing/debugging purposes.
    app.run(host='0.0.0.0', port=80, debug=True, ssl_context=context)