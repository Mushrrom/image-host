from flask import Flask, request, send_file, jsonify, render_template
import json
# import os
# from random import randint
from pages.upload import upload
from pages.view import viewimg


app = Flask(__name__)
app.register_blueprint(upload)
app.register_blueprint(viewimg)


ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

with open("config.json", "r") as f:
    json_data = json.load(f)
    URL = json_data["URL"]


@app.route('/')
def hello():
    print("hehehe")
    return 'Hello, World!'


@app.route('/b<asd>')
def catch_all(asd):
    return asd


# For hosting on the server
if __name__ == "__main__":
        app.run()
