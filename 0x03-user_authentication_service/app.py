#!/usr/bin/env python3
"""
Route module for the API
"""

from flask import Flask, jsonify, abort, request
from typing import Optional

from auth import Auth
from user import User

app: Flask = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    """App index view
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def user():
    """Register a new user
    """
    email: Optional[str] = request.form.get('email')
    password: Optional[str] = request.form.get('password')
    try:
        user: User = AUTH.register_user(email, password)
        return jsonify(
            {"email": email, "message": "user created"}
        )
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
