from flask import Flask, request, send_file, jsonify, render_template, Blueprint
import json
import os
from random import randint
import configstuff
from datetime import datetime
import random

configstuff.configsutff()
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
upload = Blueprint('upload', __name__, template_folder='templates')

URL = os.environ.get("URL")
path = os.environ.get("main_path")
data_path = os.environ.get("data_path")


def numbertobase3(n):
    if n == 0: return "0000"
    digits = ""
    while n:
        digits += str(n % 3)
        n //= 3
    while len(digits)< 4:
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


@upload.route('/upload', methods=['POST', 'GET'])
def show():
    if request.method == 'GET':
        return "get"
    else:
        [username, token, url] = [request.form["username"], request.form["token"], request.form["url"]]

        image = request.files.get("file")

        #check token and username:
        if os.path.exists(f"{data_path}/users/{username}/user.json"):
            with open(f"{data_path}/users/{username}/user.json") as info:
                infojson = json.load(info)
                if infojson["token"] == token:
                    success = 0  # success
                else:
                    success = 1  # wrong token
        else:
            success = 2  # wrong username

        if success == 0:
            if image.mimetype.startswith("image"):
                docoolstrings = True
                #Get image name string and save image
                img_name = f"{ln[randint(0, 61)]}{ln[randint(0, 61)]}{ln[randint(0, 61)]}{ln[randint(0, 61)]}"
                image.save(f'{path}/images/{username}/{image.filename}')

                # Get deletion token and save image info
                deletion_token = ''.join(random.choice(ln) for _ in range(30))
                infojson = {}
                with open(f"{data_path}/users/{username}/user.json", "r") as info:
                    infojson = json.load(info)
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
                    if docoolstrings:
                        img_name = f"‌{tocoolstring(username+img_name)}" # Has ZWNJ at start
                    else:
                        img_name = f"i{username}{img_name}"
                    img_url = f'{url}/{img_name}'
                return jsonify({"success": True, "url": img_url, "deletion_url": f"{URL}/delete/{username}{img_name}/{deletion_token}"})
        else:
            print(success)
            return jsonify({"success": False, "error_message": "Token or username or something idk"})
