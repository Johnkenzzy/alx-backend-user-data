#!/usr/bin/env python3
""" Session authentication with expiration
"""

import os
from datetime import datetime, timedelta

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session authentication with expiration time
    """

    def __init__(self):
        """Initialize and set session duration
        """
        try:
            self.session_duration = int(
                    os.getenv("SESSION_DURATION", "0"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID and store session info with timestamp
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return user_id if session is valid and not expired
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict or "user_id" not in session_dict:
            return None

        if self.session_duration <= 0:
            return session_dict["user_id"]

        if "created_at" not in session_dict:
            return None

        created_at = session_dict["created_at"]
        if created_at + timedelta(
            seconds=self.session_duration
        ) < datetime.now():
            return None

        return session_dict["user_id"]
