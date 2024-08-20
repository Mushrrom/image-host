import sqlite3
from flask import Blueprint, send_file

from consts import DATABASE

app = Blueprint('api/image/raw', __name__)


@app.route("/api/image/raw/<imageID>", methods=["GET"])
def get_raw_image(imageID):
    print(imageID, flush=True)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(f'SELECT filePath, mimeType FROM image WHERE imageID = ?', (str(imageID), ))
    record = cursor.fetchone()
    conn.close

    if not record:
        return {"success": 0, "error": "image doesnt exist"}

    filePath = record[0]
    mimeType = record[1]

    return(send_file(filePath, mimetype=mimeType))
