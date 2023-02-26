from flask import Flask, request, send_file, jsonify, render_template, Blueprint
URL = "http://127.0.0.1:5000"


viewimg = Blueprint('viewimg', __name__, template_folder='templates')


@viewimg.route('/image/<file>', methods=['GET'])
def view(file):
    return render_template("imgview.html", imgrawurl=f"{URL}/raw/image/{file}", title="test", description="test",
                           imgurl="test")


@viewimg.route('/raw/image/<file>', methods=['GET'])
def viewraw(file):
    return send_file(f"images/{file[:2]}/{file[2:]}")
    #return send_file(f"images/{file[:2]}/{file[2:]}", mimetype='image/png')
