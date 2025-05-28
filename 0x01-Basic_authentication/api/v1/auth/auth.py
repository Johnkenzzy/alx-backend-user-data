#!/usr/bin/env python3
"""Authentication model
"""

from flask import request
from typing import List, TypeVar


class Auth():
    """Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if path requires authentication
        """
        if path is None or excluded_paths is None:
            return True

        if path.endswith('/'):
            if path in excluded_paths:
                return False
            p_len: int = len(path)
            if path[:p_len - 1] in excluded_paths:
                return False
        else:
            if path in excluded_paths:
                return False
            if path + '/' in excluded_paths:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Validates all requests to secure the API
        """
        if request is None:
            return None
        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user
        """
        return None
