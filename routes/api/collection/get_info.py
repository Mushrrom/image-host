from time import time

import sqlite3
from flask import Blueprint, request

from consts import DATABASE

app = Blueprint('api/collection/get_info', __name__)

@app.route("/api/collection/<collection_id>/get_info", methods=["GET"])
def view_images(collection_id):
    # convert submitted collection ID to integer (if a user has submitted
    # something else this wont work)
    try:
        collectionID = int(collection_id)
    except:
        return {"success": 0, "error": "invalid collection ID"}

    # Get the info from the collection
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""SELECT public, collectionName FROM imageCollection
                    WHERE collectionID = ?""", (collectionID, ))
    record = cursor.fetchone()
    conn.close

    # If the collection doesnt exist and record could not be found
    if not record:
        return {"success": 0, "error": "collection does not exist"}
    collectionName = record[1]
    collectionVisibility = record[0]

    return {"success": 1, "name": collectionName, "visibility": collectionVisibility}