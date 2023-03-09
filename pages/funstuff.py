from flask import Flask, request, send_file, jsonify, render_template, Blueprint, make_response
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from io import BytesIO
from random import randint

from datetime import datetime, timedelta
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
funstuff = Blueprint('funstuff', __name__, template_folder='templates')


@funstuff.route('/88x31', methods=['POST', 'GET'])
def funtest():

    img = Image.new("RGBA", (88, 31), (0, 255, 255, 255))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype("impact.ttf", 32)
    d.text((225, 10), "Hello", font=font, fill=(0, 0, 0, 128), anchor="ma")

    for x in range(88):
        for y in range(31):
            d.point((x, y), (randint(0, 255), randint(0, 255), randint(0, 255)))

    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    response = make_response(send_file(img_io, mimetype='image/png'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = (datetime.now() - timedelta(days=1)).strftime('%a, %d %b %Y %H:%M:%S GMT')
    return response
