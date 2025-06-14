#!/usr/bin/env python3
"""Auth Module
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password string
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate uuid string
    """
    import uuid
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

    def create_session(self, email: str) -> str:
        """Create user session
        """
        try:
            user: User = self._db.find_user_by(email=email)
            session_id: str = _generate_uuid()
            setattr(user, 'session_id', session_id)
            return session_id
        except Exception:
            pass

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Retrieves the user of a session
        """
        if session_id is None:
            return None
        try:
            user: User = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Deletes user session
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Get token to reset password
        """
        try:
            user: User = self._db.find_user_by(email=email)
            token: str = _generate_uuid()
            setattr(user, 'reset_token', token)
            return token
        except NoResultFound:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """Resets user password
        """
        try:
            user: str = self._db.find_user_by(reset_token=reset_token)
            setattr(user, 'hashed_password', _hash_password(password))
            setattr(user, 'reset_token', None)
        except NoResultFound:
            raise ValueError()
