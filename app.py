import os
import secrets

from flask import Flask, jsonify, render_template, request, send_from_directory, url_for
from flask_cors import CORS

app = Flask(__name__)
app.config["UPLOAD_DIR"] = "images"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
cors = CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    file = request.files.get("image")
    file_name = secrets.token_hex(10) + os.path.splitext(file.filename)[-1]
    file.save(os.path.join(app.config["UPLOAD_DIR"], file_name))

    return jsonify({"url": url_for("images", filename=file_name, _external=True)})


@app.route("/images/<filename>")
def images(filename):
    return send_from_directory(app.config["UPLOAD_DIR"], filename)


# GUNICORN
application = app
