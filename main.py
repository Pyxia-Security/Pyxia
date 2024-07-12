#!/usr/bin/env python3

from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    # deepcode ignore RunWithDebugTrue: disable in final project, as is needed.
    app.run(host='0.0.0.0', port=80, debug=True)