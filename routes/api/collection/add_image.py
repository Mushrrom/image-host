from time import time

import sqlite3
from flask import Blueprint, request
import jwt

from consts import DATABASE, APP_SECRET_KEY

app = Blueprint('api/collection/add_image', __name__)



@app.route("/api/collection/<collection_id>/add_image", methods=["POST"])
def view_images(collection_id):
    if not "imageID" in request.form:
        return {"success": 0, "error": "invalid request"}

    try:
        imageID = int(request.form["imageID"])
    except:
        return {"success": 0, "error": "Invalid image ID"}
    # convert submitted collection ID to integer (if a user has submitted
    # something else this wont work)
    try:
        collectionID = int(collection_id)
    except:
        return {"success": 0, "error": "invalid collection ID"}

    # Check if the collection exists
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""SELECT public FROM imageCollection
                    WHERE collectionID = ?""", (collectionID, ))
    record = cursor.fetchone()
    conn.close

    if not record:
        return {"success": 0, "error": "Collection does not exist"}

    if not "token" in request.headers:
        return {"success": 0, "error": "You need to sign in to add images to this collection"}

    try:
        token = jwt.decode(request.headers["token"], APP_SECRET_KEY, algorithms=["HS256"])
    except:  # An error will occur here if the token is invalid (invalid signature, invalid data, etc)
        return {"success": 0, "error": "Invalid token - try signing in again"}

    userID = token["id"]


    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM userCollectionAllocation
                    WHERE collectionID = ? AND userID = ?""", (collectionID, userID))
    record = cursor.fetchone()
    conn.close

    # If there isnt a record here then the user doesnt have access to that
    # collection
    if not record:
        return {"success": 0, "error": "You dont have access to add images to this collection"}

    # Search the db for the provided image ID
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""SELECT ownerID FROM image WHERE imageID = ?""", (imageID, ))
    record = cursor.fetchone()
    conn.close

    if not record:
        return {"success": 0, "error": "This image doesn't exist"}

    if not record[0] == userID:
        return {"success": 0, "error": "This isn't your image"}

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO imageCollectionAllocation (imageID, collectionID)
                   VALUES (?, ?)""", (imageID, collectionID))
    conn.commit()
    conn.close

    return {"success": 1}
