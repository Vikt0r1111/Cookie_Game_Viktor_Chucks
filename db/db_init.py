import sqlite3

DB_PATH = r"db\\db.sqlite"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emails TEXT NOT NULL UNIQUE,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    conn.commit()


    cursor.execute('''
    CREATE TABLE IF NOT EXISTS upgrades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        base_price TEXT NOT NULL UNIQUE,
        cookie_pc TEXT NOT NULL UNIQUE,
        multiplier TEXT NOT NULL UNIQUE,
        quantity TEXT NOT NULL UNIQUE,
        cofficient TEXT NOT NULL UNIQUE
    )
    ''')
    conn.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_upgrades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price TEXT NOT NULL UNIQUE,
        cookie_pc TEXT NOT NULL UNIQUE,
        multiplier TEXT NOT NULL UNIQUE,
        quantity TEXT NOT NULL UNIQUE
    )
    ''')
    conn.commit()

    conn.commit()
    conn.close()
if __name__ == "__main__":
    init_db()