import sqlite3
from flask import Blueprint, send_file, render_template

from consts import DATABASE

app = Blueprint('image', __name__)

app.template_folder = "templates"
@app.route("/image/<imageID>", methods=["GET"])
def get_raw_image(imageID):
    print(imageID, flush=True)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(f'SELECT fileName, ownerID FROM image WHERE imageID = ?', (str(imageID), ))
    record = cursor.fetchone()
    if not record:
        return "image not found"
    fileName = record[0]
    userID = record[1]

    cursor.execute(f'SELECT username FROM user WHERE userID = ?', (userID, ))
    record = cursor.fetchone()
    username = record[0]
    conn.close


    return render_template("image.html", image_name = f"{fileName} uploaded by {username}",
                           image_src = f"/api/image/raw/{imageID}")
