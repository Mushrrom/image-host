from time import time

import sqlite3
from flask import Blueprint, request
import jwt

from consts import DATABASE, APP_SECRET_KEY

app = Blueprint('api/user/get_collections', __name__)

@app.route("/api/user/get_collections", methods=["GET"])
def view_images():
    if not "token" in request.headers:
        return {"auth": 0}

    try:
        token = jwt.decode(request.headers["token"], APP_SECRET_KEY, algorithms=["HS256"])
    except:  # An error will occur here if the token is invalid (invalid signature, invalid data, etc)
        return {"auth": 0}

    userID = token["id"]

    # get all the collections the user with that id has access to
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""SELECT collectionID, collectionName from imageCollection
                    WHERE collectionID IN (SELECT collectionID FROM userCollectionAllocation
                    WHERE  userCollectionAllocation.userID = ?)""",
                      (userID, ))
    record = cursor.fetchall()
    conn.close

    collections = []
    for i in record:
        collections.append({"id": i[0], "name": i[1]})

    return {"auth": 1, "collections": collections}