from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response
import configstuff
import os
import json
import random
import time

configstuff.configsutff()
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
create = Blueprint('create', __name__, template_folder='templates')

URL = os.environ.get("URL")
path = os.environ.get("main_path")
data_path = os.environ.get("data_path")
image_path = os.environ.get("images_path")
account_creation_code = "ExampleCode"
# TODO:
# [X] Make the thing add users username and password to user info thingy
# [X] Add sxcu files
@create.route('/api/create_account', methods=['POST'])
def wtf_is_the_point_of_having_useful_names_for_these():
    # Check if the request contains username and password
    if not("username" in request.form and "password" in request.form and "code" in request.form):
        return "err: need username and password and code"

    user_username = request.form["username"]
    user_password = request.form["password"]
    user_code     = request.form["code"]

    # The only username and password requirements if people want the password "a" so be it
    if len(user_username) > 30 or len(user_password) > 30:
        return "username or password too long"

    # check if user has account creation code
    if not user_code == account_creation_code:
        return "code"

    token = ''.join(random.choice(ln) for _ in range(8))
    i = 0
    username = ""
    while i == 0:
        username = f"{ln[random.randint(0, 61)]}{ln[random.randint(0, 61)]}"
        print(username)
        new_session_token = ''.join(random.choice(ln) for _ in range(20))
        if not os.path.exists(f"{data_path}/users/{username}"):
            # os.mkdir(f"{data_path}/users/{username}")
            # os.mkdir(f"{data_path}/users/{username}/images")
            os.mkdir(f"{image_path}/{username}")
            with open(f"{data_path}/users/{username}/user.json", "w") as f:
                data = {"token": token,
                        "storage_used": 0,
                        "uploads": 0,
                        "user_name": user_username,
                        "user_password": user_password,
                        "creationdate": time.time(),
                        "settings": {
                            "embed": {
                                "title": "{filename} - {filesize}",
                                "description": "{user_storage} uploaded in {user_uploads} images by this user "
                            }},
                        "user_level": 1,
                        "auth": {
                            "session_tokens": {
                                f"{new_session_token}": time.time()
                            }
                        }
                        }
                i = 1
                json.dump(data, f)


    return jsonify({"success": 1, "session_token": new_session_token})