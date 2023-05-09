import json

from flask import Flask, request, send_file, jsonify, render_template, Blueprint
import os
import configstuff
import urllib.parse

configstuff.configsutff()

URL = os.environ.get("URL")
path = os.environ.get("main_path")
data_path = os.environ.get("data_path")
image_path = os.environ.get("images_path")
viewimg = Blueprint('viewimg', __name__, template_folder='templates')

ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


def tokb(inp):
    a = True
    times = 0
    # Convert to kb/mb/gb
    while a:
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

    rettitle = user_embed_settings["title"].format(filename=filename, filesize=size, user_storage=user_size,
                                                   user_uploads=user_uploads)

    retdescription = user_embed_settings["description"].format(filename=filename, filesize=size, user_storage=user_size,
                                                               user_uploads=user_uploads)

    return render_template("imgview.html", imgrawurl=f"{URL}/api/image/raw/{file[:2]}{filename}",
                           title=str(rettitle),
                           description=str(retdescription),
                           imgurl="test3")


# For zero width characters: For if you are using an editor that doesn't show, this is @viewimg.route("/[ZWNJ]<file")
@viewimg.route("/‌<file>")
def viewzerowidth(file):
    filestring = urllib.parse.quote(file).split("%E2%80%8")[1:]  # Now it will just be a list like ["B", "C", "D"]
    filestring = [filestring[i:i + 4] for i in range(0, len(filestring), 4)]
    if not len(filestring[-1]) == 4:
        return "err: Filstring not divisible by 3"

    imagestring = ""
    base_3_dict = {'B': 0, 'C': 1, 'D': 2}
    # This whole thing is base 3
    # B is 0
    # C is 1
    # D is 2

    for i in filestring:
        n = 0
        # Convert to base 10
        for j, c in enumerate(i[::-1]):
            n += base_3_dict[c] * (3 ** j)

        try:
            imagestring += ln[n]
        except:
            return "Image string wrong idk what you did"

    print(imagestring)
    return view(imagestring)


@viewimg.route('/image/<file>', methods=['GET'])
def viewold(file):
    return view(file)


@viewimg.route('/api/image/raw/<file>', methods=['GET'])
def viewraw(file):
    return send_file(f"{image_path}/{file[:2]}/{file[2:]}")
    # return send_file(f"images/{file[:2]}/{file[2:]}", mimetype='image/png')
