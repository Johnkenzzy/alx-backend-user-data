#!/usr/bin/env python3
"""Basic Auth module
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Basic Authentication
    """
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The full Authorization
            header.

        Returns:
            str: The Base64-encoded credentials string,
            or None if invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]
