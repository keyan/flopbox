import os
from hashlib import sha1

from flask import Flask, request


app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.path.realpath(__file__)


@app.route('/', methods=['GET'])
def index():
    return 'index'


@app.route('/file_list', methods=['POST'])
def file_list():
    return file_list


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        print file


@app.route('/download', methods=['GET'])
def download():
    pass


if __name__ == "__main__":
    file_dict = {}
    app.debug = True
    app.run()
