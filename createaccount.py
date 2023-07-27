import os
import sys
import random
import time

from pymongo import MongoClient

import configstuff
# may need to run: chmod 777 -R ./ after running this
# This is for creating accounts on the server idk if I will create a better way to do this
# okay i understand this is bad and i am gonna add it to the server


def get_database():
    '''connect to db'''
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)

    return client["image-host"]


configstuff.configsutff()
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"


collection_name = get_database()["users"]

data_path = os.environ.get("data_path")
images_path = os.environ.get("images_path")

token = sys.argv[1]


uid = ""


if len(sys.argv) == 2:
    i = 0
    while i == 0:
        uid = f"{ln[random.randint(0, 61)]}{ln[random.randint(0, 61)]}"
        usr = collection_name.find_one({"uid" : uid})

        if not usr:
            os.mkdir(f"{images_path}/{uid}")
            data = {
	            "version": 1,
                "username": "example_username",
                "uid": uid,
                "upload_token" : token,
                "upload_stats": {
                    "storage_used": 0,
                    "uploads": 0,
                },
                "settings": {
                   "display_name": "example_displayname",
                    "embed": {
                        "title": "{filename} - {filesize}",
                        "description": "{user_storage} uploaded in {"
                            "user_uploads} images by this user ",
                        "colour": "#FF6EC4"
                    }
                },
                "creation_date" : time.time(),
                "user_level" : 1,         
            }
            collection_name.insert_one(data)
            i = 1
#
# if len(sys.argv) == 2:
#     i = 0
#     while i == 0:
#         username = f"{ln[random.randint(0, 61)]}{ln[random.randint(0, 61)]}"
#         if not os.path.exists(f"{data_path}/users/{username}"):
#             os.mkdir(f"{data_path}/users/{username}")
#             os.mkdir(f"{data_path}/users/{username}/images")
#             os.mkdir(f"{images_path}/{username}")
#             with open(f"{data_path}/users/{username}/user.json", "w") as f:
#                 data = {"token": token, "storage_used": 0, "uploads": 0, "public_name": "example",
#                         "creationdate": time.time(), "settings": {
#                         "embed": {
#                             "title": "{filename} - {filesize}",
#                             "description": "{user_storage} uploaded in {"
#                                            "user_uploads} images by this user "
#                         }},
#                         "user_level": 1
#
#                         }
#                 i = 1
#                 json.dump(data, f)
# else:
#     username = sys.argv[2]
#     if not os.path.exists(f"{data_path}/users/{username}"):
#         os.mkdir(f"{data_path}/users/{username}")
#         os.mkdir(f"{data_path}/users/{username}/images")
#         os.mkdir(f"{images_path}/{username}")
#         with open(f"{data_path}/users/{username}/user.json", "w") as f:
#             data = {"token": token, "storage_used": 0, "uploads": 0, "public_name": "example",
#                     "creationdate": time.time(), "settings": {
#                     "embed": {
#                         "title": "{filename} - {filesize}",
#                         "description": "{user_storage} uploaded in {"
#                                        "user_uploads} images by this user "
#                     }}
#                     }
#             json.dump(data, f)
#     else:
#         print("Username already used")
#         quit()

print(f"created account with username: {uid} and token: {token}")
