import re
import random
import hashlib
from time import time

import sqlite3
from flask import Blueprint, request

from consts import DATABASE, CHARACTERS

app = Blueprint('api/user/sign_up', __name__)

@app.route("/api/user/sign_up", methods=["POST"])
def sign_up():
# Handle requests that are missing username or password
    if not "username" in request.form or not "password" in request.form or not "email" in request.form:
        return {"success": 0, "error": "Invalid request"}

    username = request.form["username"]
    password = request.form["password"]
    email    = request.form["email"]

    # prevent SQL injection :3
    if not re.match(r'^[a-z0-9_-]+$', username):
        return {"success": 0, "error": "invalid username"}

    # generate hash of password
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        uploadKey = ''.join(random.choice(CHARACTERS) for _ in range(8))

        cursor.execute(f'INSERT INTO user (username, passwordHash, userEmail, uploadKey) VALUES (?, ?, ?, ?)', (username, password_hash, email, uploadKey))
        conn.commit()
        conn.close

    # This will happen if an error occurs due to a username or email not being unique
    except:
        return {"success": 0, "error": "could not create record - maybe your username or email is in use"}

    return {"success": 1}