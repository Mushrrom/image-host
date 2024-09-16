"""So why is there a second upload function?
This is basically the other upload function, but set up for use directly from
the web browser using the users session token (JWT), where as the other one
uses a special upload key to be integrated with other services such as shareX
"""

from time import time
import random
import sqlite3

import jwt
from flask import Blueprint, request, Response, jsonify
from PIL import Image
from consts import DATABASE, URL, APP_SECRET_KEY

app = Blueprint('api/image/upload', __name__)

def convert_to_jpg(input_path, output_path):
    with Image.open(input_path) as img:
        # Resizes the image while keeping same aspect ratio
        max_size = (512, 512)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # converts the image to RGB mode because thats what jpg needs
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Save it as JPG format
        img.save(output_path, format="JPEG")

@app.route("/api/image/upload", methods=["POST"])
def upload():
    # Checking token and stuff
    if not "token" in request.headers:
        return {"success": 0, "error": "You need to sign in to change the visibility of this collection"}

    try:
        token = jwt.decode(request.headers["token"], APP_SECRET_KEY, algorithms=["HS256"])
    except:  # An error will occur here if the token is invalid (invalid signature, invalid data, etc)
        return {"success": 0, "error": "Invalid token - try signing in again"}

    userID = token["id"]

    image = request.files.get("image")

    # Add image to db
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    imageID = random.randint(0, 99999999)

    cursor.execute('INSERT INTO image (imageID, fileName, mimeType, ownerID, filePath)'
                   ' VALUES (?,  ?, ?, ?, ? )',
                    (str(imageID), str(image.filename), str(image.mimetype), int(userID), f"images/{imageID}"))
    record = cursor.fetchone()
    conn.commit()
    conn.close

    # Save the image
    image.save(f"images/{imageID}")

    # Save the thumbnail
    convert_to_jpg(f"images/{imageID}", f"images/{imageID}_THUMBNAIL")

    return {"success": 1, "url": f"{URL}/image/{imageID}"}


