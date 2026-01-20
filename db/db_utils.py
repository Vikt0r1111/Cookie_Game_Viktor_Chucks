import sqlite3
from utils import data_chacher

def insert_user_data(db_path, username, password):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO users (username, password)
    VALUES (?, ?)
    ''', (username, password))

    conn.commit()
    conn.close()

def check_user(db_path, username, password):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?',
                       (username, password))
        row = cursor.fetchone()

    if row is not None:
        return True
    else:
        return False

def get_user(username):
    conn = sqlite3.connect("db/db.sqlite")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    row = cursor.fetchone()

    conn.close()




    