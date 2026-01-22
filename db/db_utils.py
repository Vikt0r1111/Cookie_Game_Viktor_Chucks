import sqlite3
from config.upgrades import UPGRADES

def insert_user_data(db_path, username, password, email):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO users (username, password, emails)
    VALUES (?, ?, ?)
    ''', (username, password, email))

    user_id = cursor.lastrowid

    for upgrade in UPGRADES:
        cursor.execute(
            "INSERT OR IGNORE INTO upgrades (name) VALUES (?)",
            (upgrade,)
        )
    
    conn.commit()
    conn.close()

def check_user(db_path, email, password):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE emails=? AND password=?',
                       (email, password))
        row = cursor.fetchone()

    if row is not None:
        return True
    else:
        return False

def get_user(username):
    conn = sqlite3.connect("db/db.sqlite")
    cursor = conn.cursor()

    if username == "all":
        cursor.execute("SELECT * FROM users")
        row = cursor.fetchall()
        return row
    
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    row = cursor.fetchall()
    conn.close()
    return row

def get_user_by_email(email):
    conn = sqlite3.connect("db/db.sqlite")
    cursor = conn.cursor()

    cursor.execute('SELECT username FROM users WHERE emails=?', (email,))
    row = cursor.fetchone()
    conn.close()
    return row


    