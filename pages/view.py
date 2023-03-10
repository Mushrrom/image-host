import json

from flask import Flask, request, send_file, jsonify, render_template, Blueprint
import os
import configstuff
configstuff.configsutff()

URL = os.environ.get("URL")
path = os.environ.get("main_path")
data_path = os.environ.get("data_path")
image_path = os.environ.get("images_path")
print(image_path)
viewimg = Blueprint('viewimg', __name__, template_folder='templates')

def tokb(inp):
    a = True
    times = 0
    while a == True:
        if inp/1000 >= 1:
            inp = inp/1000
            times += 1
        else:
            a = False
    stuff = ["B", "KB", "MB", "GB", "TB"]
    out = f"{round(inp, 2)} {stuff[times]}"
    return out


@viewimg.route('/image/<file>', methods=['GET'])
def view(file):
    [size, upload_time, filename, user_size, user_uploads] = ["", {}, "", "", ""]
    with open(f"{data_path}/users/{file[:2]}/images/{file[2:6]}.json", "r") as f:
        fjson = json.load(f)
        size = fjson["size"]
        upload_time = fjson["timeinfo"]
        filename = fjson["filename"]

    with open(f"{data_path}/users/{file[:2]}/user.json", "r") as f:
        fjson = json.load(f)
        user_size = fjson["storage_used"]
        user_uploads = fjson["uploads"]
        user_embed_settings = fjson["settings"]["embed"]
    print(f"{filename} - {str(tokb(int(size)))}")
    # rettitle = f"{filename} - {tokb(int(size))}"
    # retdescription = f"{tokb(int(user_size))} uploaded in {user_uploads} images by this user"
    rettitle = user_embed_settings["title"].replace("{filename}", filename)
    rettitle = rettitle.replace("{filesize}", tokb(int(size)))
    rettitle = rettitle.replace("{user_storage}", tokb(int(user_size)))
    rettitle = rettitle.replace("{user_uploads}", str(user_uploads))

    retdescription = user_embed_settings["title"].replace("{filename}", filename)
    retdescription = retdescription.replace("{filesize}", tokb(int(size)))
    retdescription = retdescription.replace("{user_storage}", tokb(int(user_size)))
    retdescription = retdescription.replace("{user_uploads}", str(user_uploads))
    print(rettitle)
    return render_template("imgview.html", imgrawurl=f"http://{URL}/raw/image/{file}",
                           title=str(rettitle),
                           description=str(retdescription),
                           imgurl="test3")

@viewimg.route('/raw/image/<file>', methods=['GET'])
def viewraw(file):
    print(f"{image_path}/{file[:2]}/{file[2:]}")
    return send_file(f"{image_path}/{file[:2]}/{file[2:]}")
    #return send_file(f"images/{file[:2]}/{file[2:]}", mimetype='image/png')
