from flask import Flask
import os
import hashlib


app = Flask(__name__)


@app.route('/')
def index():
    return 'TODO'

if __name__ == "__main__":
    app.debug = True
    app.run()
