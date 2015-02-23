#!/usr/bin/env python

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

# Configuration
UPLOAD_FOLDER = os.path.abspath('.') + '/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "Upload complete."
        return "There was a problem with the file upload requested."


@app.route('/download/', methods=['GET'])
def download():
    return "<h1>This is the download page</h1>"


if __name__ == "__main__":
    file_dict = {}
    app.debug = True
    app.run()
