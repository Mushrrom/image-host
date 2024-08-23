import re
import hashlib
from time import time

import sqlite3
from flask import Blueprint, request
import jwt

from consts import DATABASE, APP_SECRET_KEY

app = Blueprint('api/user/get_images', __name__)

@app.route("/api/user/get_images", methods=["GET"])
def view_images():
    if not "token" in request.headers:
        return {"auth": 0}

    try:
        token = jwt.decode(request.headers["token"], APP_SECRET_KEY, algorithms=["HS256"])
    except:  # An error will occur here if the token is invalid (invalid signature, invalid data, etc)
        return {"auth": 0}

    userID = token["id"]

    # get the images linked to the user
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""SELECT imageID, fileName FROM image
                    WHERE image.ownerID = ?""", (userID, ))
    record = cursor.fetchall()
    conn.close

    # Format the records into a better format
    images = []
    for i in record:
        images.append({"id": i[0], "name": i[1]})

    return {"success": 1, "images": images}