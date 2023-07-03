from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from io import BytesIO
from random import randint

from datetime import datetime, timedelta
public = Blueprint('public', __name__, template_folder='templates')


@public.route('/', methods=['POST', 'GET'])
def site_root():
    return send_file("public/login/login.html")

@public.route("/public/<path:pars>")
def public_slash(pars):
    print(pars)
    return send_file(f"public/{pars}")