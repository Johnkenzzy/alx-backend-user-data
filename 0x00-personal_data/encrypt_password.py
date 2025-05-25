#!/usr/bin/env python3
"""Encrypt_password module
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password with a randomly-generated salt using bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if a provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
