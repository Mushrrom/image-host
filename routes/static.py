from flask import Blueprint, send_file, render_template

app = Blueprint('static', __name__)

app.template_folder = "templates"
@app.route("/", methods=["GET"])
def root():
    return send_file("static/index.html")

@app.route("/index.js")
def index_js():
    return send_file("static/index.js")

@app.route("/all_images")
def all_images():
    return send_file("static/all_images.html")

@app.route("/all_images.js")
def all_images_js():
    return send_file("static/all_images.js")

@app.route("/my_collections")
def my_collections():
    return send_file("static/my_collections.html")

@app.route("/my_collections.js")
def my_collections_js():
    return send_file("static/my_collections.js")