import json

from flask import Flask, request, send_file, jsonify, render_template, Blueprint
import os
import configstuff
configstuff.configsutff()

URL = os.environ.get("URL")
path = os.environ.get("main_path")
data_path = os.environ.get("data_path")
viewimg = Blueprint('viewimg', __name__, template_folder='templates')



@viewimg.route('/image/<file>', methods=['GET'])
def view(file):
    with open(f"{data_path}/users/{file[:2]}/images/{file[2:]}.json}", "r") as f:
        fjson = json.load(f)
        size = fjson["size"]
        upload_time = fjson["timeinfo"]
        filename = fjson["filename"]
        # TODO:
        #   - Add title and stuff
        #   - other stuff 
    return render_template("imgview.html", imgrawurl=f"http://{URL}/raw/image/{file}", title="test1", description="test2",
                           imgurl="test3")


@viewimg.route('/raw/image/<file>', methods=['GET'])
def viewraw(file):
    return send_file(f"{path}/images/{file[:2]}/{file[2:]}")
    #return send_file(f"images/{file[:2]}/{file[2:]}", mimetype='image/png')
