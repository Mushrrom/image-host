from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response
import configstuff
import os
import json

configstuff.configsutff()
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
create = Blueprint('create', __name__, template_folder='templates')

URL = os.environ.get("URL")
path = os.environ.get("main_path")
data_path = os.environ.get("data_path")


@create.route('/api/create_account', methods=['POST'])
def show():
    [test] = [request.form["test"]]
    print("a")
    print(test)
    return "b"