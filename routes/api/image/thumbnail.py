import sqlite3
from flask import Blueprint, send_file

from consts import DATABASE

app = Blueprint('api/image/thumbnail', __name__)


@app.route("/api/image/thumbnail/<imageID>", methods=["GET"])
def get_raw_image(imageID):
    print(imageID, flush=True)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(f'SELECT filePath FROM image WHERE imageID = ?', (str(imageID), ))
    record = cursor.fetchone()
    conn.close

    if not record:
        return {"success": 0, "error": "image doesnt exist"}

    filePath = record[0]

    return(send_file(f"{filePath}_THUMBNAIL", mimetype="image/jpeg"))
