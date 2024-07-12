#!/usr/bin/env python3
from flask import Flask, render_template, redirect, request, session, abort
from testdatabase import *
import os, flask_login
from flask_login import current_user
from database import Userdb, db
from decouple import config

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///{config("NAME")}:{config("PASSWORD")}@localhost:{config("PORT")}/{config("DATABASE")}"
db.init_app(app)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

with app.app_context():
    db.create_all()

@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return
    user = User()
    user.id = username
    return user

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return
    
    user = User()
    user.id = username
    return user

@app.route("/", methods=['GET', 'POST'])
def index():
    session['error'] = "False"
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if current_user.is_authenticated == True:
            return redirect('/')
        if 'error' in session:
            if session['error'] == "True":
                return render_template("login.html", error=True)
            else:
                return render_template("login.html", error=False)
        return render_template("login.html", error=False)
    username = request.form.get('username')
    if username in users and request.form.get('password') == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        session['error'] = "False"
        return redirect('/')
    session['error'] = "True"
    return redirect('/login')

@app.route('/logout')
def logout():
    session['error'] = "False"
    flask_login.logout_user()
    return redirect('/')

@app.route('/signup')
def signup():
    session['error'] = "False"
    if current_user.is_authenticated == True:
            return redirect('/') 
    return render_template("signup.html")

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

@app.errorhandler(Exception)
def unauthorized_handler(e):
    return render_template("error/418.html", error=e), 418

@app.route("/teapot")
def teapoteasteregg():
    abort(405)

if __name__ == "__main__":
    # deepcode ignore RunWithDebugTrue: disable debug in final project, as is for testing/debugging purposes.
    app.run(host='0.0.0.0', port=80, debug=True)