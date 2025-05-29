#!/usr/bin/env python3
"""Authentication model
"""

import os
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

        normalized_paths = {path.rstrip('/') for path in excluded_paths}
        path = path.rstrip('/')

        for excluded_path in normalized_paths:
            if excluded_path is None:
                continue

            if excluded_path.endswith('*'):
                # Wildcard match: check if path starts with the base pattern
                base = excluded_path[:-1]
                if path.startswith(base):
                    return False
            else:
                if path == excluded_path:
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

    def session_cookie(self, request=None):
        """Gets a cookie value from a request
        """
        if not request:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
