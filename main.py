import os

from flask import Flask, request, send_file, jsonify, render_template
import json
# import os
# from random import randint
from pages.upload import upload
from pages.view import viewimg
from pages.funstuff import funstuff
from pages.delete import delete
import urllib.parse
import configstuff

configstuff.configsutff()


app = Flask(__name__)
app.register_blueprint(upload)
app.register_blueprint(viewimg)
app.register_blueprint(funstuff)
app.register_blueprint(delete)

ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

URL = os.environ.get("URL")


@app.route('/')
def hello():
    print("hehehe")
    return 'Hello, World!'


@app.route('/b<asd>')
def catch_all(asd):
    print(urllib.parse.quote(asd))
    return asd



# For hosting on the server
if __name__ == "__main__":
        app.run()
