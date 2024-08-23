import re
import random
import hashlib
from time import time

import sqlite3
from flask import Blueprint, request

from consts import DATABASE

app = Blueprint('api/user/login', __name__)

@app.route("/api/user/login", methods=["POST"])
def login():
    # Handle requests that are missing username or password
    if not "username" in request.form or not "password" in request.form:
        return {"success": 0, "error": "Invalid request"}

    username = request.form["username"]
    password = request.form["password"]

    # prevent SQL injection :3
    if not re.match(r'^[a-z0-9_-]+$', username):
        return {"success": 0, "error": "invalid username"}

    # generate hash of password
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Search for user in db and check sumitted password matches
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(f'SELECT passwordHash, userID FROM user WHERE username = "{request.form["username"]}"')
    record = cursor.fetchone()
    conn.close

    # If user doesnt exist
    if not record:
        return {"success": 0, "error": "Invalid username or password"}

    user_password = record[0]
    userID = record[1]



    # If password isnt correct
    if not user_password == password_hash:
        return {"success": 0, "error": f"Invalid username or password"}

    # Generate new session & save key
    session_key = str(random.randint(0,10000000000)) # TODO fix this shit

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(f'INSERT INTO token (userID, value, createdDate)'
                   f' VALUES ({userID}, {session_key}, {int(time())})')
    conn.commit()
    conn.close

    return {"success": 1, "session_key": session_key}
