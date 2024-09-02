#!/usr/bin/env python3
from flask import Flask, render_template, redirect, request, session, abort
import os, flask_login, shutil
from flask_login import current_user
from database import db, Mapped, mapped_column
from decouple import config
from lib.flask_recaptcha import ReCaptcha
from pathlib import Path
from post_creator import scan_upload, create_list, create_post, total_posts, change_post_total_by_one, create_post_folder, file_mime_type, change_post_total_by_minus_one
from user_agents import parse

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{config("NAME")}:{config("PASSWORD")}@localhost:{config("PORT")}/{config("DATABASE")}"
app.config["RECAPTCHA_SECRET_KEY"] = config("RECAPTCHA_SECRET_KEY")
app.config["RECAPTCHA_SITE_KEY"] = config("RECAPTCHA_SITE_KEY")
app.config["RECAPTCHA_ENABLED"] = config("RECAPTCHA_ENABLED")
app.config['UPLOAD_FOLDER'] = "C:\\Digi Project - Social Media\\Pyxia\\posts\\"
recaptcha = ReCaptcha(app=app)
db.init_app(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
total_post = total_posts()

class User(db.Model, flask_login.UserMixin):
    __tablename__ = "userdb"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str]

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
    return render_template("main.html", yes=session["device_type"])

@app.route("/notifications", methods=['GET'])
def notifications_page():
    return render_template("notifications.html")

@app.route("/pyxia", methods=['GET'])
def scroll():
    session['error'] = False
    session['already_exists'] = False
    session['robot'] = False
    if current_user.is_authenticated == False:
            return redirect('/')
    return render_template("index.html")

#def check_sessionvar_exist(variable):
 #   if variable in session:
   #     if session[f"{variable}"] != "":
  #          return True
        
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
def home():
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
                if user.password == request.form.get('password'):
                    flask_login.login_user(user)
                    session['error'] = "False"
                    session['robot'] = False
                    return redirect('/')
                else:
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
    session['error'] = False
    session['already_exists'] = False
    session['robot'] = False
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
            email = request.form.get('email')
            username = request.form.get('username')
            chkemail = check_email(email)
            if chkemail == True or chkemail == "True":
                session['already_exists'] = True
                return redirect('/signup')
            chkusr = check_user(username)
            if chkusr == True or chkusr == "True":
                session['already_exists'] = True
                return redirect('/signup')
            if request.form.get('password') != request.form.get('confirm-password'):
                session['error'] = True
                return redirect('/signup')
            else:
                session['error'] = False
                session['already_exists'] = False
                session['robot'] = False
                user = User(
                    email=email,
                    username=username,
                    password=request.form.get('password')
                )
                db.session.add(user)
                db.session.commit()
                return redirect('/login-ert')
        else:
            session['robot'] = True
            redirect('/signup')

@app.route('/pyxia/upload', methods=['POST'])
def file_upload():
    files = request.files.getlist("file")
    post_id = total_posts()
    create_post_folder(post_id)
    change_post_total_by_one()
    if str(files) == str("[<FileStorage: '' ('application/octet-stream')>]") or files == "":
        images = 0
        print("no images")
    else:
        images = len(files)
        file_list = []
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
            else:
                post_path = Path(f"posts/{post_id}")
                shutil.rmtree(post_path)
                change_post_total_by_minus_one()
                print("Post_error")
                return('error')
            print("File type: ",file_type)
            time_through += 1
            file_list.append(os.path.join(app.config["UPLOAD_FOLDER"], f"{post_id}", f"post{time_through}{file_type}"))
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], f"{post_id}", f"post{time_through}{file_type}"))
            mime = file_mime_type(os.path.join(app.config["UPLOAD_FOLDER"], f"{post_id}", f"post{time_through}{file_type}"))
            print("mime")
            if mime not in mimes:
                print("not in mimes")
                post_path = Path(f"posts/{post_id}")
                shutil.rmtree(post_path)
                change_post_total_by_minus_one()
                return('error')
            scan_result = scan_upload(os.path.join(app.config["UPLOAD_FOLDER"], f"{post_id}", f"post{time_through}{file_type}"))
            if scan_result == "malware":
                print("malware")
                post_path = Path(f"posts/{post_id}")
                print(post_path)
                shutil.rmtree(post_path)
                change_post_total_by_minus_one()
                return('error')
    temp_list = create_list(post_id, request.form.get("title"), request.form.get("description"), current_user.username, current_user.id, 0, request.form.get("private"), file_list, images, request.form.get('age_rating'))
    response = create_post(temp_list)
    if response == "completed":
        return redirect('/pyxia')
    else:
        return('error')
    
@app.route('/pyxia/upload_test', methods=['GET'])
def test_file_upload():
    if current_user.is_authenticated == False:
        return redirect('/')
    return render_template("test_upload.html")
    
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
 #   return render_template("error/418.html", error=e), 418

@app.route("/teapot")
def teapoteasteregg():
    abort(405)

if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    # deepcode ignore RunWithDebugTrue: disable debug in final project, as is for testing/debugging purposes.
    app.run(host='0.0.0.0', port=80, debug=True, ssl_context=context)