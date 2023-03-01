from flask import Flask, request, send_file, jsonify, render_template, Blueprint
import os
import configstuff
configstuff.configsutff()

URL = os.environ.get("URL")
path = os.environ.get("main_path")

viewimg = Blueprint('viewimg', __name__, template_folder='templates')



@viewimg.route('/image/<file>', methods=['GET'])
def view(file):
    return render_template("imgview.html", imgrawurl=f"http://{URL}/raw/image/{file}", title="test", description="test",
                           imgurl="test")


@viewimg.route('/raw/image/<file>', methods=['GET'])
def viewraw(file):
    return send_file(f"{path}/images/{file[:2]}/{file[2:]}")
    #return send_file(f"images/{file[:2]}/{file[2:]}", mimetype='image/png')
