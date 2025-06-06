#!/usr/bin/env python3
"""
Route module for the API
"""

from flask import (
    Flask, jsonify, abort, request,
    make_response, Response, redirect, url_for
)
from typing import Optional

from auth import Auth
from user import User

app: Flask = Flask(__name__)
AUTH: Auth = Auth()


@app.route('/', methods=['GET'])
def index() -> str:
    """App index view
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def user() -> str:
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


@app.route('/sessions', methods=['POST'])
def login() -> Response:
    """Login a user
    """
    email: Optional[str] = request.form.get('email')
    password: Optional[str] = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id: Optional[str] = AUTH.create_session(email)
        resp: Response = make_response(
            jsonify(
                {"email": email, "message": "logged in"}
            )
        )
        resp.set_cookie('session_id', session_id)
        return resp
    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> Response:
    """Logout user
    """
    session_id: Optional[str] = request.cookies.get('session_id')
    user: Optional[User] = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('index'))
    abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> Response:
    """Get user details
    """
    session_id: Optional[str] = request.cookies.get('session_id')
    user: Optional[User] = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> Response:
    """Get token to reset user password
    """
    email: Optional[str] = request.form.get('email')
    try:
        token: str = AUTH.get_reset_password_token(email)
        if token:
            return jsonify(
                {"email": email, "reset_token": token}
            ), 200
    except ValueError():
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> Response:
    """Update user password
    """
    email: Optional[str] = request.form.get('email')
    new_password: Optional[str] = request.form.get('new_password')
    reset_token: Optional[str] = request.form.get('reset_token')
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify(
            {"email": email, "message": "Password updated"}
        ), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
