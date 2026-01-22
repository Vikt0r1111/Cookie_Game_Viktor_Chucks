import os
from flask.sessions import SecureCookieSessionInterface
from flask import Flask, render_template, request, session, redirect
from dotenv import load_dotenv

from utils import data_chacher, translate_text
from db import insert_user_data, check_user, get_user, get_user_by_email

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def index():
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        return "No session cookie", 400
    serializer = SecureCookieSessionInterface().get_signing_serializer(app)
    data = serializer.loads(session_cookie)
    email = data.get('email')
    print(email)
    return render_template("home.html")

@app.route("/cookiet_game", methods=["GET", "POST"])
def cookie_game():
    return render_template("game.html")

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        hashed_password = data_chacher(password)
        print("DEBUG:", username, hashed_password, email)
        insert_user_data("db/db.sqlite", username, hashed_password, email)
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = data_chacher(password)
        print("DEBUG:", email, hashed_password)

        if check_user("db/db.sqlite", email, hashed_password):
            session["email"] = email
            return redirect("/")
        else:
            return "incorect login of password", 401

        
    return render_template("login.html")

@app.route("/admin_panel/", methods=["GET", "POST"])
def admin_panel():
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        return "No session cookie", 400
    serializer = SecureCookieSessionInterface().get_signing_serializer(app)
    data = serializer.loads(session_cookie)
    email = data.get('email')
    username_uf = get_user_by_email(email)
    username = username_uf[0]
    if username != "admin":
        print(username)
        return redirect("/login")
    
    user_list = get_user("all")
    print(user_list)
    return render_template("admin.html",
    users=user_list
    )

@app.route("/privacy-policy/<language>", methods=["GET"])
def privacy_policy(language):
    privacy_policy = translate_text("config\\privacy-policy.txt", language)
    return render_template("privacy_policy.html",
    privacy_policy = privacy_policy
    )

if __name__ == "__main__":
    app.run(host="localhost", port="8000", debug=True)