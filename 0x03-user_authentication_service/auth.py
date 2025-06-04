#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password string
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user
        """
        if self._db.find_user_by(email=email):
            raise ValueError(f'user {email} already exists.')
        hashedpw: bytes = _hash_password(password)
        user: User = self._db.add_user(email, hashedpw)
        return user
