from flask import Flask, request, send_file, jsonify, render_template, Blueprint
import json
import os
from random import randint
import configstuff
from datetime import datetime
import random
from pymongo import MongoClient


configstuff.configsutff()
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
upload = Blueprint('upload', __name__, template_folder='templates')

URL = os.environ.get("URL")
path = os.environ.get("main_path")
data_path = os.environ.get("data_path")
images_path = os.environ.get("images_path")
def get_database():
    '''connect to db'''
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)

    return client["image-host"]

def numbertobase3(n):
    if n == 0: return "0000"
    digits = ""
    while n:
        digits += str(n % 3)
        n //= 3
    while len(digits) < 4:
        digits += "0"
    return digits[::-1]


def tocoolstring(input):
    # Input is just the name of the image e.g aA1234
    retstring = ""
    for i in list(input):
        # Basically just converts it to base 3 then uses that to make the image
        e = numbertobase3(ln.index(i))
        # ZWSP ZWNJ ZWJ in this variable
        invischars = "​‌‍"
        for j in e:
            retstring += invischars[int(j)]

    return retstring


@upload.route('/api/upload', methods=['POST', 'GET'])
def show():
    if request.method == 'GET':
        return "get"

    db_client = get_database()
    db_users = db_client["users"]
    db_images = db_client["images"]

    url = request.form["url"]
    token = request.form["auth"][2:]
    username = request.form["auth"][:2]
    print(token)
    print(username)
    image = request.files.get("file")

    user = db_users.find_one({"uid": username})

    # check token and username:
    if not user:
        return jsonify({"success": False, "error_message": "Username does not exist"}), 400
    if not user["upload_token"] == token:
        return jsonify({"success": "false", "error_message": "Wrong token"}), 400

    print("user found with token")
    

    if not image.mimetype.startswith("image"):
        return jsonify({"success": False, "error_message": "Upload an image"}), 400

    # update user stats
    db_users.update_one({"uid": username},
                        {"$inc": {"upload_stats.uploads": 1,
                                  "upload_stats.storage_used": os.fstat(image.fileno()).st_size}})


    img_name = ''.join(random.choice(ln) for _ in range(2))
    image.save(f"{images_path}/{username}/{img_name}")

    deletion_token = ''.join(random.choice(ln) for _ in range(30))
    cd = datetime.now()  # cd = current date

    db_images.insert_one({"size": os.fstat(image.fileno()).st_size,
                          "date": str(datetime.now()),
                          "timeinfo": {
                             "year": cd.year,
                             "month": cd.month,
                             "day": cd.day,
                             "hour": cd.hour,
                             "minute": cd.minute,
                             "second": cd.second
                        },
                          "owner": username,
                          "image_id": img_name,
                          "image_mimetype": image.mimetype,
                          "filename": image.filename,
                          "already_image_exists": False,
                          "deletion_token": deletion_token,
                        })
   
    
    img_url = f"{url}/{username}{img_name}"
    print("ret")
    return jsonify({"success": True, "url": img_url,
                        "deletion_url": f"{URL}/api/delete/{img_name}/{deletion_token}"})


    # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    if image.mimetype.startswith("image"):
        docoolstrings = False
        # Get image name string and save image
        img_name = f"{ln[randint(0, 61)]}{ln[randint(0, 61)]}{ln[randint(0, 61)]}{ln[randint(0, 61)]}"
        image.save(f'{path}/images/{username}/{image.filename}')

        # Get deletion token and save image info
        deletion_token = ''.join(random.choice(ln) for _ in range(30))
        with open(f"{data_path}/users/{username}/user.json", "r") as info:
            infojson: any = json.load(info)
            infojson["uploads"] += 1
            infojson["storage_used"] += os.fstat(image.fileno()).st_size

        with open(f"{data_path}/users/{username}/user.json", "w") as info:
            json.dump(infojson, info)

        with open(f"{data_path}/users/{username}/images/{img_name}.json", "w") as f:
            cd = datetime.now()  # cd = current date
            infojson = {"size": os.fstat(image.fileno()).st_size,
                        "date": str(datetime.now()),
                        "timeinfo": {
                            "year": cd.year,
                            "month": cd.month,
                            "day": cd.day,
                            "hour": cd.hour,
                            "minute": cd.minute,
                            "second": cd.second
                        },
                        "filename": image.filename,
                        "already_image_exists": False,
                        "deletion_token": deletion_token,
                        }
            json.dump(infojson, f)

            # Get url to return to user
            img_name = f"{username}{img_name}"
            if docoolstrings:
                img_url = f'{url}/‌{tocoolstring(img_name)}'  # URL has ZWNJ after the {url}/
            else:
                img_url = f'{url}/i{img_name}'
        return jsonify({"success": True, "url": img_url,
                        "deletion_url": f"{URL}/api/delete/{img_name}/{deletion_token}"})

