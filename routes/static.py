from flask import Blueprint, send_file, render_template

app = Blueprint('static', __name__)

app.template_folder = "templates"
@app.route("/", methods=["GET"])
def root():
    return send_file("static/index.html")

@app.route("/index.js")
def index_js():
    return send_file("static/index.js")