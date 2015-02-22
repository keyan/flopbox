# flopbox Server
#
# Handles file sync
#
# Run this in a different directory than client.py:
# python server.py
#
# Author(s): Keyan Pishdadian (and maybe Noah Ennis)

import os
from hashlib import sha1

from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.path.abspath('.') + '/uploads'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return 'GET request'
    if request.method == 'POST':
        return 'POST request'


@app.route('/file_list/', methods=['POST'])
def file_list():
    return 'file_list'


@app.route('/upload/', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'FILE UPLOADED'
        return 'POST request'


@app.route('/download/', methods=['GET'])
def download():
    return "<h1>This is the download page</h1>"


@app.route('/test_post/', methods=['POST'])
def test_post():
    return "it worked!"


if __name__ == "__main__":
    file_dict = {}
    app.debug = True
    app.run()
