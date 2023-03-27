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


@upload.route('/upload', methods=['POST', 'GET'])
def show():
    # okay but python is not slow at all this crap takes less than 0.01 seconds wtf
    if request.method == 'GET':
        return "get"
    else:
        [username, token, url] = [request.form["username"], request.form["token"], request.form["url"]]

        image = request.files.get("file")
        # Save the image to disk

        if os.path.exists(f"{data_path}/users/{username}/user.json"):
            with open(f"{data_path}/users/{username}/user.json") as info:
                infojson = json.load(info)
                if infojson["token"] == token:
                    success = 0  # success
                else:
                    success = 1  # wrong token
        else:
            success = 2  # wrong token
        # lol i hope this random code wasn't important

        if success == 0:
            if image.mimetype.startswith("image"):
                print(image.filename)
                img_name = f"{ln[randint(0, 61)]}{ln[randint(0, 61)]}{ln[randint(0, 61)]}{ln[randint(0, 61)]}"
                image.save(f'{path}/images/{username}/{image.filename}')
                img_url = f'{url}/i{username}{img_name}.{image.filename.split(".")[-1]}'

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
                return jsonify({"success": True, "url": img_url, "deletion_url": f"{URL}/delete/{username}{img_name}/{deletion_token}"})
        else:
            print(success)
            return jsonify({"success": False, "error_message": "Token or username or something idk"})
