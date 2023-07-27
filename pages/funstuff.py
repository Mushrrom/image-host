from io import BytesIO
from random import randint
from datetime import datetime, timedelta

from flask import send_file, Blueprint, make_response
from PIL import Image, ImageDraw
ln = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
funstuff = Blueprint('funstuff', __name__, template_folder='templates')


@funstuff.route('/88x31', methods=['POST', 'GET'])
def funtest():

    img = Image.new("RGBA", (88, 31), (0, 255, 255, 255))
    d = ImageDraw.Draw(img)

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
