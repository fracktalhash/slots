import hashlib
import os
import secrets
import sqlite3


def hash_password(password) -> str:
    """
    Creates a random salt and Hashes the password using sha512.
    Done so that passwords are stored securely in the Database
    """
    salt = secrets.token_bytes(18)  # Generates a stream of random bits using the CSPRNG
    hashed = hashlib.sha512(salt + password.encode()).digest()  # Salts and hashes the password
    return salt.hex() + ":" + hashed.hex()  # Returns the salt:hashed_password in hex


def init_db():
    """Called when the table needs to created"""
    with sqlite3.connect("users.db") as conn:  # Opens connection and
        c = conn.cursor()  # Sets c as the cursor for interacting with the sqlite db
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")  # Double checks for the table in the db
        if not c.fetchone():  # If no table is found
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS users
                (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL UNIQUE,
                PASSWORD TEXT NOT NULL,
                BANK REAL DEFAULT 0.0,
                SPIN_COUNT INTEGER DEFAULT 0);
                """
            )  # Creates the table and columns
        conn.commit()  # Saves changes


def check_username(name) -> bool:
    while True:
        try:
            with sqlite3.connect("users.db") as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE NAME = ?", (name,))  # Looks for the user's desired username
                if c.fetchone():
                    return False  # If the username is found return 'False' the user cannot use this username
                else:
                    return True  # If the username is not found return 'True" the user can use this username
        except sqlite3.OperationalError:
            init_db()
            continue


def create_account(name, password, bank) -> tuple[str, tuple[int, int]]:
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        password_hashed = hash_password(password)  # Sets up the salt:passwordhash combo
        c.execute(
            "INSERT INTO users (NAME, PASSWORD) VALUES (?, ?)", (name, password_hashed)
        )  # Inserts the name and salt:passwordhash combo into the table
        c.execute("UPDATE users SET BANK = ? WHERE NAME = ?", (bank, name))  # Writes the deposit into the table
        conn.commit()
        return login(name, password)  # Auto logs in the user returns tuple (name,(bank,spin_count)) sets up the player object


def login(name, password) -> tuple[str, tuple[int, int]] | bool | int:
    """Authenticates the user and returns the data needed to build the player object"""
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        try:
            c.execute("SELECT PASSWORD FROM users WHERE NAME=?", (name,))  # Looks for the username to grab the password
            user = c.fetchone()  # Put the result in a variable called user
            if user:  # If the username is found
                spass = user[0]  # Grab the password from the user variable
                salt_hex, hash_hex = spass.split(":")  # Split the salt:passwordhash combo at the (:)
                salt = bytes.fromhex(salt_hex)  # Turn the salt back to byte stream
                cpass = hashlib.sha512(
                    salt + password.encode()
                ).digest()  # Hash the password provided by the user with the stored hash from the salt:passwordhash combo
                if hash_hex == cpass.hex():  # If the hashed user provided password matches the stored hashed password
                    c.execute("SELECT BANK, SPIN_COUNT FROM users WHERE NAME=?", (name,))  # Pull the "account" information bank and spin_count
                    user_data = c.fetchone()  # Places the result in the variable user_data
                    return name, user_data  # Return the name and the user_data

                else:  # If the passwords don't match return False user is not authenticated
                    return False

            else:  # If there is no username found return False user is not authenticated
                return False

        except sqlite3.OperationalError:  # If there is an SQL operational error
            os.system("cls" if os.name == "nt" else "clear")  # Clear the terminal
            print("No table found. Is this the first time running the game?")  # Let the user know that the table was not found
            user_input = input(
                "Press '1' to retry, or '2' to initialize: "
            )  # Allow the user to try again or go through the registration loop  and create the user table in the process
            if user_input.strip() == "2":  # If the user selects to initialize the db and register
                init_db()  # run the db initialization function
                return "2"  # Return "2" so the user can jump to the registration loop


def account_updater(name, bank=None, spin_count=None):
    """
    Stores user's data as the game is played.
    Mainly the current numbers of spins and the user's running bank
    """
    with sqlite3.connect("users.db") as conn:
        c = conn.cursor()
        if bank < 1:  # If the bank is less then one namely zero
            c.execute("DELETE FROM users WHERE NAME = ?", (name,))  # The user has lost so delete their information
        if bank is not None and spin_count is not None:  # When the user spins
            c.execute(
                "UPDATE users SET BANK = ?, SPIN_COUNT=?  WHERE NAME = ?",
                (bank, spin_count, name),
            )  # New Bank & spin_count values are stored
        conn.commit()  # Save the data
