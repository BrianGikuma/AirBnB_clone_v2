#!/usr/bin/python3
"""Hello route module"""
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    """Hello route"""
    return 'Hello HBNB!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
