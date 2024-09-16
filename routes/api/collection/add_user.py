from time import time

import sqlite3
from flask import Blueprint, request
import jwt

from consts import DATABASE, APP_SECRET_KEY

app = Blueprint('api/collection/add_user', __name__)



@app.route("/api/collection/<collection_id>/add_user", methods=["POST"])
def add_user(collection_id):
    if not "userID" in request.form:
        return {"success": 0, "error": "invalid request"}

    # convert submitted collection ID to integer (if a user has submitted
    # something else this wont work)
    try:
        collectionID = int(collection_id)
    except:
        return {"success": 0, "error": "invalid collection ID"}

    try:  # convert submitted user ID to int (same as above)
        submitted_userID = int(request.form["userID"])
    except:
        return {"success": 0, "error": "Invalid user ID"}

    # Check if the collection exists
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM imageCollection
                    WHERE collectionID = ?""", (collectionID, ))
    record = cursor.fetchone()
    conn.close

    if not record:
        return {"success": 0, "error": "Collection does not exist"}

    if not "token" in request.headers:
        return {"success": 0, "error": "You need to sign in to add users to this collection"}

    try:
        token = jwt.decode(request.headers["token"], APP_SECRET_KEY, algorithms=["HS256"])
    except:  # An error will occur here if the token is invalid (invalid signature, invalid data, etc)
        return {"success": 0, "error": "Invalid token - try signing in again"}

    userID = token["id"]

    # Search for records where the collectionId and userId are equal to provided
    # values
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM userCollectionAllocation
                    WHERE collectionID = ? AND userID = ?""", (collectionID, userID))
    record = cursor.fetchone()
    conn.close

    # If there isnt a record here then the user doesnt have access to that
    # collection
    if not record:
        return {"success": 0, "error": "You dont have access to add users to this collection"}

    # If nothing else has had an error we can add the user
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO userCollectionAllocation (userID, collectionID)
                   VALUES (?, ?)""", (submitted_userID, collectionID))
    conn.commit()
    conn.close

    return {"success": 1}
