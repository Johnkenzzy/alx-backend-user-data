#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password string
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid():
    """Generate uuid string
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f'user {email} already exists.')
        except NoResultFound:
            hashedpw: bytes = _hash_password(password)
            user: User = self._db.add_user(email, hashedpw)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials
        """
        try:
            user: User = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False
