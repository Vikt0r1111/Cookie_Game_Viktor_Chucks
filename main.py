import os
from flask.sessions import SecureCookieSessionInterface
from flask import Flask, render_template, request, session, redirect
from dotenv import load_dotenv

from utils import data_chacher
from db import insert_user_data, check_user, get_user

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def index():
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        return "No session cookie", 400
    serializer = SecureCookieSessionInterface().get_signing_serializer(app)
    data = serializer.loads(session_cookie)
    username = data.get('username')
    print(username)
    return f"<h1>{username}</h1>"

@app.route("/cookiet_game", methods=["GET", "POST"])
def cookie_game():
    return 

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        hashed_password = data_chacher(password)
        print("DEBUG:", username, hashed_password)
        insert_user_data("db/db.sqlite", username, hashed_password)
    
    return render_template("registration.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        hashed_password = data_chacher(password)
        print("DEBUG:", username, hashed_password)

        if check_user("db/db.sqlite", username, hashed_password):
            session["username"] = username
            return redirect("/")
        else:
            return "incorect login of password", 401

        
    return render_template("login.html")

@app.route("/admin_panel", methods=["GET", "POST"])
def admin_panel():
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        return "No session cookie", 400
    serializer = SecureCookieSessionInterface().get_signing_serializer(app)
    data = serializer.loads(session_cookie)
    username = data.get('username')
    if username != "admin":
        return redirect("/login")
    
    user_list = get_user("all")
    print(user_list)
    return render_template("admin.html",
    users=user_list
    )

if __name__ == "__main__":
    app.run(host="localhost", port="8000", debug=True)