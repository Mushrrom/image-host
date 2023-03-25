import json

from flask import Flask, request, send_file, jsonify, render_template, Blueprint
import os
import configstuff

configstuff.configsutff()

URL = os.environ.get("URL")
path = os.environ.get("main_path")
data_path = os.environ.get("data_path")
image_path = os.environ.get("images_path")
viewimg = Blueprint('viewimg', __name__, template_folder='templates')


def tokb(inp):
    a = True
    times = 0
    while a == True:
        if inp / 1000 >= 1:
            inp = inp / 1000
            times += 1
        else:
            a = False
    stuff = ["B", "KB", "MB", "GB", "TB"]
    out = f"{round(inp, 2)} {stuff[times]}"
    return out


@viewimg.route('/i<file>', methods=['GET'])
def view(file):
    [size, upload_time, filename, user_size, user_uploads] = ["", {}, "", "", ""]
    if not os.path.exists(f"{data_path}/users/{file[:2]}/images/{file[2:6]}.json"): return "no image"
    with open(f"{data_path}/users/{file[:2]}/images/{file[2:6]}.json", "r") as f:
        fjson = json.load(f)
        size = tokb(int(fjson["size"]))
        upload_time = fjson["timeinfo"]
        filename = fjson["filename"]

    with open(f"{data_path}/users/{file[:2]}/user.json", "r") as f:
        fjson = json.load(f)
        user_size = tokb(int(fjson["storage_used"]))
        user_uploads = fjson["uploads"]
        user_embed_settings = fjson["settings"]["embed"]
    # rettitle = f"{filename} - {tokb(int(size))}"
    # retdescription = f"{tokb(int(user_size))} uploaded in {user_uploads} images by this user"

    rettitle = user_embed_settings["title"].format(filename=filename, filesize=size, user_storage=user_size,
                                                   user_uploads=user_uploads)

    retdescription = user_embed_settings["description"].format(filename=filename, filesize=size, user_storage=user_size,
                                                         user_uploads=user_uploads)

    return render_template("imgview.html", imgrawurl=f"{URL}/raw/image/{file[:2]}{filename}",
                           title=str(rettitle),
                           description=str(retdescription),
                           imgurl="test3")


@viewimg.route('/image/<file>', methods=['GET'])
def viewold(file):
    return view(file)

@viewimg.route('/raw/image/<file>', methods=['GET'])
def viewraw(file):
    return send_file(f"{image_path}/{file[:2]}/{file[2:]}")
    # return send_file(f"images/{file[:2]}/{file[2:]}", mimetype='image/png')
