#!/usr/bin/env python

# flopbox Server
#
# Handles file sync
#
# Run this in a different directory than client.py:
# python server.py
#
# TODO:
# - Web UI
# - Stop using relative paths (line 23/25)
#
# Author: Keyan Pishdadian

import os
import json

from flask import Flask, request, render_template, send_from_directory
from werkzeug import secure_filename

# Configuration
UPLOAD_FOLDER = os.path.abspath('.') + '/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return 'POST request'

    return render_template("index.html")


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename,
                               as_attachment=True)


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


@app.route('/file_list/', methods=['GET'])
def file_list():
    files = _list_files()
    return json.dumps(files)


@app.route('/delete/<filename>', methods=['GET'])
def delete(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    finally:
        return "Done"


def _list_files():
    """
    Return a list containing all non-hidden files in the current directory.
    """
    files = [file for file in next(os.walk(app.config['UPLOAD_FOLDER']))[2]
             if not file[0] == '.']
    return files


if __name__ == "__main__":
    file_dict = {}
    app.debug = True
    app.run()
