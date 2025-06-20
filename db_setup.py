import sqlite3
import hashlib
import os

def hash_password(password):

    salt = os.urandom(18)
    hashed = hashlib.sha512(salt + password.encode()).digest()

    return salt.hex() + ':' + hashed.hex()

def create_user(name, password, bank):

    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='users';
        """)

        if not c.fetchone():
            print("DB exists, but 'users' table is missing.\n. . . intitializing 'users' table")
            c.execute('''
                CREATE TABLE IF NOT EXISTS users
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL UNIQUE,
                PASSWORD TEXT NOT NULL,
                BANK REAL NOT NULL,
                SPIN_COUNT INTEGER NOT NULL DEFAULT 0);
            ''')
            print("Database initialized.")

        c.execute('SELECT * FROM users WHERE NAME = ?', (name,))

        if c.fetchone():
            print(f"Username {name} is taken. Please select a new one.")
            return False

        password = hash_password(password)
        c.execute(
            "INSERT INTO users (NAME, PASSWORD, BANK) VALUES (?, ?, ?)",
            (name, password, bank))
        conn.commit()
        print(f"Account created successfully for {name}.")

        return True

def login(name,password):

    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        c.execute("SELECT PASSWORD, BANK, SPIN_COUNT FROM users WHERE NAME=?", (name,))
        spass, BANK, SPIN_COUNT = c.fetchone()
        result = c.fetchone()

        if not result:
            print("Wrong username or password")
            return False

        spass, BANK, SPIN_COUNT = result
        salt_hex, hash_hex = spass.split(':')
        salt = bytes.fromhex(salt_hex)
        cpass = hashlib.sha512(salt + password.encode()).digest()

        if hash_hex == cpass.hex():
            print(f"You are logged in as {name}")
            return True, name, BANK, SPIN_COUNT

        else:
            print("Wrong username or password")
            return False