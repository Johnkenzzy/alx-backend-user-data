#!/usr/bin/env python3
"""Test Main
"""

import requests

BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """Test user registration."""
    resp = requests.post(
        f"{BASE_URL}/users", data={"email": email, "password": password}
    )
    if resp.status_code == 200:
        print("User registered successfully.")
    elif resp.status_code == 400 and "already registered" in resp.text:
        print("User already registered.")
    else:
        assert False, f"Unexpected registration response: {resp.status_code} - {resp.text}"


def log_in_wrong_password(email: str, password: str) -> None:
    """Test login with wrong password."""
    resp = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert resp.status_code == 401, f"Expected 401, got {resp.status_code}"


def log_in(email: str, password: str) -> str:
    """Test login and return session_id."""
    resp = requests.post(
        f"{BASE_URL}/sessions", data={"email": email, "password": password}
    )
    assert resp.status_code == 200
    assert "session_id" in resp.cookies
    return resp.cookies["session_id"]


def profile_unlogged() -> None:
    """Test accessing profile without being logged in."""
    resp = requests.get(f"{BASE_URL}/profile")
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """Test accessing profile while logged in."""
    cookies = {"session_id": session_id}
    resp = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert resp.status_code == 200
    assert "email" in resp.json()


def log_out(session_id: str) -> None:
    """Test user logout."""
    cookies = {"session_id": session_id}
    resp = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert resp.status_code == 302  # Redirect to /


def reset_password_token(email: str) -> str:
    """Test generating a reset token."""
    resp = requests.post(
        f"{BASE_URL}/reset_password", data={"email": email}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "reset_token" in data
    return data["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Test updating password with reset token."""
    resp = requests.put(
        f"{BASE_URL}/reset_password",
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password
        }
    )
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "Password updated"}


# Test credentials
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
