from flask import Flask, request, send_file, jsonify, render_template, Blueprint
import json
import os
from random import randint
import configstuff
configstuff.configsutff()
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
upload = Blueprint('upload', __name__, template_folder='templates')

URL = os.environ.get("URL")
path = os.environ.get("main_path")


@upload.route('/upload', methods=['POST', 'GET'])
def show():
    if request.method == 'GET':
        print(request)
        return "get"
    else:
        [username, token, url] = [request.form["username"], request.form["token"], request.form["url"]]

        image = request.files.get("file")
        print(image.filename)
        print(path)
        # Save the image to disk
        with open(f"{path}/data.json", "r") as info:
            infojson = json.load(info)
            print(infojson["users"])
            if infojson["users"][username]:
                if infojson["users"][username]["token"] == token:
                    success = 0 #success
                else: success = 1 #wrong token
            else: success = 2 #wrong username

        if success == 0:
            if image.mimetype.startswith("image"):
                img_name = f"{ln[randint(0, 61)]}{ln[randint(0, 61)]}{ln[randint(0, 61)]}{ln[randint(0, 61)]}"
                image.save(f'{path}/images/{username}/{img_name}.{image.filename.split(".")[-1]}')
                img_url = f'{url}/image/{username}{img_name}.{image.filename.split(".")[-1]}'
                print(os.fstat(image.fileno()).st_size)
                return jsonify({"success": True, "url": img_url})
        else:
            return jsonify({"success": False, "error_message": "Token or username or something idk"})
