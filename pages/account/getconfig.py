from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response
import configstuff
import os
import json
import random
import time
import tempfile

configstuff.configsutff()
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
getconfig = Blueprint('getconfig', __name__, template_folder='templates')

url = os.environ["URL"]
@getconfig.route('/api/account/config/<auth>', methods=['GET'])
def getconfigg(auth):
    temp_file = tempfile.mktemp(suffix=".sxcu")
    rendered_template = render_template("config.sxcu", url=url, auth=auth)
    with open(temp_file, 'w') as f:
        f.write(rendered_template)

    return send_file(temp_file, as_attachment=True)