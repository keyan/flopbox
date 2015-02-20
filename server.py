from flask import Flask
import os
from hashlib import sha1


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return 'TODO'


@app.route('/file_list', methods=['POST'])
def file_list():
    return file_list


@app.route('/upload', methods=['POST'])
def upload():
    pass

def make_file_dict():
    """
    Returns a dictionary containing as keys, all the non-hidden files in the
    current directoy, and as values, their sha1 hashes.
    """
    file_list = [file for file in next(os.walk('.'))[2] if not file[0] == '.']

    file_dict = {}
    for file in file_list:
        file_dict[file] = sha1(open(file, 'rb').read())

    return file_dict


if __name__ == "__main__":
    file_dict = {}
    app.debug = True
    app.run()
