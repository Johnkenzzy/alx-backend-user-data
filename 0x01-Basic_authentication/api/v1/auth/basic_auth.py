#!/usr/bin/env python3
"""Basic Auth module
"""

import base64

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

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """
        Decodes a Base64-encoded string to UTF-8.

        Args:
            base64_authorization_header (str): Base64 string to decode.

        Returns:
            str: Decoded UTF-8 string, or None if input is invalid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            decoded_bytes = base64.b64decode(base64_bytes)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Extracts user credentials from the decoded Base64 header.

        Args:
            decoded_base64_authorization_header (str):
            Decoded "user:password" string.

        Returns:
            tuple: (user_email, password) or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email = decoded_base64_authorization_header.split(':', 1)
        password = decoded_base64_authorization_header.split(':', 1)
        return user_email, password
