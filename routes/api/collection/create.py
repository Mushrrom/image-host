from time import time

import sqlite3
from flask import Blueprint, request
import jwt

from consts import DATABASE, APP_SECRET_KEY

app = Blueprint('api/collection/create', __name__)



@app.route("/api/collection/create", methods=["POST"])
def view_images():
    if not "collectionName" in request.form:
        return {"success": 0, "error": "invalid request"}

    collectionName = request.form["collectionName"]

    # Checking token and stuff
    if not "token" in request.headers:
        return {"success": 0, "error": "You need to sign in to change the visibility of this collection"}

    try:
        token = jwt.decode(request.headers["token"], APP_SECRET_KEY, algorithms=["HS256"])
    except:  # An error will occur here if the token is invalid (invalid signature, invalid data, etc)
        return {"success": 0, "error": "Invalid token - try signing in again"}

    userID = token["id"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO imageCollection (collectionName, public)
                   VALUES (?, ?)""", (collectionName, 0))
    collectionID = cursor.lastrowid

    cursor.execute("""INSERT INTO userCollectionAllocation (userID, collectionID)
                   VALUES (?, ?)""", (userID, collectionID))
    conn.commit()
    conn.close

    return {"success": 1}