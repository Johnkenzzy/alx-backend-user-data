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
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path is None:
                continue

            if excluded_path.endswith('*'):
                # Wildcard match: check if path starts with the base pattern
                base = excluded_path[:-1]
                if path.startswith(base):
                    return False
            else:
                # Normalize and compare both with and without trailing slash
                if not excluded_path.endswith('/'):
                    excluded_path += '/'
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
