from time import time

import sqlite3
from flask import Blueprint, request
import jwt

from consts import DATABASE, APP_SECRET_KEY

app = Blueprint('api/collection/get_images', __name__)


def get_collection_images(collectionID):
    """A function to get all of the images stored in a collection
    This is needed because we dont need to check user ID if the collection is
    public

    Args:
        collectionID (int): ID of the collection
    """
    # Get all the images that are stored in the collection
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""SELECT imageID, fileName FROM image
                    WHERE imageID IN (SELECT imageID FROM imageCollectionAllocation
                    WHERE collectionID=?)""", (collectionID, ))
    record = cursor.fetchall()
    conn.close
    images = []
    for i in record:
        images.append({"id": i[0], "name": i[1]})

    return images


@app.route("/api/collection/<collection_id>/get_images", methods=["GET"])
def view_images(collection_id):
    # convert submitted collection ID to integer (if a user has submitted
    # something else this wont work)
    try:
        collectionID = int(collection_id)
    except:
        return {"success": 0, "error": "invalid collection ID"}

    # Check if the DB is public
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""SELECT public, collectionName FROM imageCollection
                    WHERE collectionID = ?""", (collectionID, ))
    record = cursor.fetchone()
    conn.close

    if not record:
        return {"success": 0, "error": "Collection does not exist"}

    collectionName = record[1]
    public = record[0]

    # If the collection is public the record will return 1 and we can just
    # return the collection straight to the user
    if public == 1:
        return {"success": 1, "images": get_collection_images(collectionID), "collectionName": collectionName, "public": public}

    # Everything else here is if the collection is private
    if not "token" in request.headers:
        return {"success": 0, "error": "You need to sign in to access this collection"}

    # If the token is nothing that will be because the fetch cookie function in
    # the front end returned an empty string, meaning the user has not signed in
    # and there is no token
    if request.headers["token"] == "":
        return {"success": 0, "error": "You need to sign in to access this collection"}

    try:
        token = jwt.decode(request.headers["token"], APP_SECRET_KEY, algorithms=["HS256"])
    except:  # An error will occur here if the token is invalid (invalid signature, invalid data, etc)
        return {"success": 0, "error": "Invalid token - try signing in again"}

    userID = token["id"]

    # By just searching for allocations where the userID and the collectionID
    # are both there it is easy to check the record
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM userCollectionAllocation
                    WHERE collectionID = ? AND userID = ?""", (collectionID, userID))
    record = cursor.fetchone()
    conn.close

    # If there isnt a record here then the user doesnt have access to that
    # collection
    if not record:
        return {"success": 0, "error": "You dont have access to this collection"}

    return {"success": 1, "images": get_collection_images(collectionID), "collectionName": collectionName, "public": public}