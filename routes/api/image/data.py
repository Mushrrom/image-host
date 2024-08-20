import sqlite3
from flask import Blueprint, send_file

from consts import DATABASE

app = Blueprint('api/image/data', __name__)


@app.route("/api/image/data/<imageID>", methods=["GET"])
def get_raw_image(imageID):
    print(imageID, flush=True)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(f'SELECT fileName, ownerID FROM image WHERE imageID = ?', (str(imageID), ))
    record = cursor.fetchone()
    fileName = record[0]
    userID = record[1]

    cursor.execute(f'SELECT username FROM user WHERE userID = ?', (userID, ))
    record = cursor.fetchone()
    username = record[0]
    conn.close


    return({"username": username, "fileName": fileName})
