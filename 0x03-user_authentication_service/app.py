#!/usr/bin/env python3
"""
Route module for the API
"""

from flask import Flask, jsonify, abort, request


app: Flask = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """App index view
    """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
