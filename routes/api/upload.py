from time import time
import re
import uuid
import hashlib
import random

import sqlite3
from flask import Blueprint, request, Response, jsonify
from PIL import Image
from consts import DATABASE, URL

app = Blueprint('api/upload', __name__)

mime_types = {
    "image/apng": ".apng",
    "image/avif": ".avif",
    "image/bmp": ".bmp",
    "image/gif": ".gif",
    "image/vnd.microsoft.icon": ".ico",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/svg+xml": ".svg",
    "image/tiff": ".tiff",
    "image/webp": ".webp",
}

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

@app.route("/api/upload", methods=["POST"])
def upload():
    print("upload", flush=True)
    if not "token" in request.form:
        # need to return this as a string to make shareX happy :)
        return Response(str({"error_message": "no token provided"}), status=400,
                         mimetype='application/json')

    # Get token from request form and image from request file
    token = request.form["token"]
    image = request.files.get("image")

    # Prevent SQL injection on token (should only have these values)
    if not re.match(r'^[A-z0-9_-]+$', token):
        print(token, flush=True)
        return Response(str({"error_message": "invalid token"}), status=400,
                         mimetype='application/json')


    # Find user that matches token
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # print(token, flush=True)
    # TODO: check this wonnt have sql injection problems
    cursor.execute("SELECT userID FROM user WHERE uploadKey = ? ;", (str(token), ))
    record = cursor.fetchone()
    conn.close

    userID = record[0]
    # print(record, flush=True)

    # If user with token cant be found
    if not record:
        return Response(str({"error_message": "invalid token2"}), status=400,
                         mimetype='application/json')

    print(image.mimetype, flush=True)

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

    return {"url": f"{URL}/image/{imageID}"}


