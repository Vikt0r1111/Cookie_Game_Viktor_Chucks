import os
from flask.sessions import SecureCookieSessionInterface
from flask import Flask, render_template, request, session, redirect

from utils import data_chacher, translate_text, add_user, get_user_data, make_click, update_click, buy_upgrade, buy_levelup
from db import insert_user_data, check_user, get_user, get_user_by_email, get_user_id, get_user_id_mails

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def index():
    session_cookie = request.cookies.get("session")
    if not session_cookie:
        return redirect("/login")
    serializer = SecureCookieSessionInterface().get_signing_serializer(app)
    data = serializer.loads(session_cookie)
    email = data.get('email')
    username = get_user_by_email(email)
    usernamef = username[0]
    return render_template("home.html", username=usernamef)

@app.route("/cookie_game", methods=["GET", "POST"])
def game():
    email = session.get("email")
    if not email:
        session.clear()
        return redirect("/login")

    user_id = get_user_id_mails(email)
    if not user_id:
        session.clear()
        return redirect("/login")

    if request.method == "POST":
        user_data = get_user_data(str(user_id))
        if not user_data:
            session.clear()
            return redirect("/login")

        return user_data
    username = get_user_by_email(email)

    return render_template("game.html", username=username[0])

@app.route("/click", methods=["POST"])
def click():
    if request.method == "POST":
        session_cookie = request.cookies.get("session")
        if not session_cookie:
            return "No session cookie", 400
        serializer = SecureCookieSessionInterface().get_signing_serializer(app)
        data = serializer.loads(session_cookie)
        email = data.get('email')
        id = get_user_id_mails(email)
        make_click(str(id))
    return {
        "status": "ok"
    }, 200

@app.route("/upgrade_click", methods=["POST"])
def upgrade_post():
    if request.method == "POST":
        session_cookie = request.cookies.get("session")
        if not session_cookie:
            return "No session cookie", 400
        serializer = SecureCookieSessionInterface().get_signing_serializer(app)
        data = serializer.loads(session_cookie)
        email = data.get('email')
        id = get_user_id_mails(email)
        update_click(id)
        return {
        "status": "ok"
    }, 200

@app.route("/buy_upgrades", methods=["POST"])
def buy_upgrades():
    if request.method == "POST":
        upgrade_name = request.form.get("upgrade_name")
        session_cookie = request.cookies.get("session")
        if not session_cookie:
            return "No session cookie", 400
        serializer = SecureCookieSessionInterface().get_signing_serializer(app)
        data = serializer.loads(session_cookie)
        email = data.get('email')
        id = get_user_id_mails(email)
        buy_upgrade(upgrade_name, str(id))
        return {
            "status": "ok"
        }, 200
    
@app.route("/buy_levelup", methods=["POST"])
def buy_levelups():
    if request.method == "POST":
        upgrade_name = request.form.get("upgrade_name")
        session_cookie = request.cookies.get("session")
        if not session_cookie:
            return "No session cookie", 400
        serializer = SecureCookieSessionInterface().get_signing_serializer(app)
        data = serializer.loads(session_cookie)
        email = data.get('email')
        id = get_user_id_mails(email)
        buy_levelup(id, upgrade_name)
        return {
            "status": "ok"
        }, 200

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        hashed_password = data_chacher(password)
        print("DEBUG:", username, hashed_password, email)
        try:
            insert_user_data("db/db.sqlite", username, hashed_password, email)
        except Exception as e:
            error = "accaunt with this email or username already exists"
            return render_template("register.html", error=error)
        id = get_user_id(username)
        add_user(id)
        succes = True
        if succes:
            return redirect("/login")
        else:
            return redirect("/registration")


    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = data_chacher(password)
        print("DEBUG:", email, hashed_password)

        if check_user("db/db.sqlite", email, hashed_password):
            session["email"] = email
            return redirect("/")
        else:
            error = "Email or password is incorrect"

    return render_template("login.html", error=error)

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/login")


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
    app.run(host="127.0.0.1", port="8000", debug=True)