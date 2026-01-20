from flask import Flask, render_template, request, session, redirect
from db import insert_user_data, check_user
from utils import data_chacher, secret_key_generator, decode_base64, session_cutter
import os
from dotenv import load_dotenv



app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    full_session = session.get("username")
    first_part = session_cutter(full_session) if full_session else None
    username = decode_base64(first_part)
    return username

@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Заполните все поля", 400

        hashed_password = data_chacher(password)
        print("DEBUG:", username, hashed_password)
        insert_user_data("db/db.sqlite", username, hashed_password)
    
    return render_template("registration.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Заполните все поля", 400

        hashed_password = data_chacher(password)
        print("DEBUG:", username, hashed_password)

        if check_user("db/db.sqlite", username, hashed_password):
            session["username"] = username
            return redirect("/")
        else:
            return "incorect login of password", 401

        
    return render_template("login.html")


if __name__ == "__main__":
    app.run(host="localhost", port="8000", debug=True)