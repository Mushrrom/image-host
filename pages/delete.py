from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response
import configstuff
import os
import json
#for deleting files

configstuff.configsutff()
from datetime import datetime, timedelta
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
delete = Blueprint('delete', __name__, template_folder='templates')


data_path = os.environ["data_path"]
images_path = os.environ["images_path"]

@delete.route('/api/delete/<img>/<token>', methods=['POST', 'GET'])
def deleteimage(img, token):
    if not os.path.exists(f"{data_path}/users/{img[:2]}/images/{img[2:6]}.json"): return "image does not exist"
    image_deletion_token = ""
    fjson = {}
    with open(f"{data_path}/users/{img[:2]}/images/{img[2:6]}.json", "r") as f:
        fjson = json.loads(f.read())
        image_deletion_token = fjson["deletion_token"]

    if image_deletion_token == token:

        imgsize = 0
        with open(f"{data_path}/users/{img[:2]}/images/{img[2:6]}.json", "r") as f:
            fjson = json.loads(f.read())
            img_name = fjson["filename"]
            imgsize = int(fjson["size"])

        fjson = {}
        with open(f"{data_path}/users/{img[:2]}/user.json", "r") as f:
            fjson = json.loads(f.read())

        fjson["storage_used"] -= imgsize

        with open(f"{data_path}/users/{img[:2]}/user.json", "w") as f:
            json.dump(fjson, f)
        os.remove(f"{images_path}/{img[:2]}/{img_name}")
        os.remove(f"{data_path}/users/{img[:2]}/images/{img[2:6]}.json")
        return "deleted image"
    else:
        return "wrong token >:("
#PEP 8: W292 no newline at end of file
#PEP 8: E265 block comment should start with '# '
