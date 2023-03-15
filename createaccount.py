import os
import sys
import configstuff
import random
import json
import time
# This is for creating accounts on the server idk if I will create a better way to do this
configstuff.configsutff()

ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

data_path = os.environ.get("data_path")
images_path = os.environ.get("images_path")
print(data_path)

token = sys.argv[1]

if not os.path.exists(f"{data_path}/users"):
    print("creating users directory")
    os.mkdir(f"{data_path}/users")

username = ""

if len(sys.argv) == 2:
    i = 0
    while i == 0:
        username = f"{ln[random.randint(0, 61)]}{ln[random.randint(0, 61)]}"
        if not os.path.exists(f"{data_path}/users/{username}"):
            os.mkdir(f"{data_path}/users/{username}")
            os.mkdir(f"{data_path}/users/{username}/images")
            os.mkdir(f"{images_path}/{username}")
            with open(f"{data_path}/users/{username}/user.json", "w") as f:
                data = {"token": token, "storage_used": 0, "uploads": 0, "public_name": "example",
                    "creationdate": time.time(), "settings": {
                                                              "embed": {
                                                                  "title": "{filename} - {filesize}",
                                                                  "description": "{user_storage} uploaded in {"
                                                                                 "user_uploads} images by this user "
                                                              }}
                    }
            i = 1
            json.dump(data, f)
else:
    username = sys.argv[2]
    if not os.path.exists(f"{data_path}/users/{username}"):
        os.mkdir(f"{data_path}/users/{username}")
        os.mkdir(f"{data_path}/users/{username}/images")
        os.mkdir(f"{images_path}/{username}")
        with open(f"{data_path}/users/{username}/user.json", "w") as f:
            data = {"token": token, "storage_used": 0, "uploads": 0, "public_name": "example",
                    "creationdate": time.time(), "settings": {
                                                              "embed": {
                                                                  "title": "{filename} - {filesize}",
                                                                  "description": "{user_storage} uploaded in {"
                                                                                 "user_uploads} images by this user "
                                                              }}
                    }
            json.dump(data, f)
    else:
        print("Username already used")
        quit()


print(f"created account with username: {username} and token: {token}")

