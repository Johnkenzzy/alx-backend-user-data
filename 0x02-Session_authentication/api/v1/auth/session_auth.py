#!/usr/bin/env python3
"""Session Authentication module
"""

import uuid
from typing import Dict

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session authentication class
    """
    user_id_by_session_id: Dict = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates session
        """
        if not user_id or not isinstance(user_id, str):
            return None
        session_id: str = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Gets the user of a particular session
        """
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)
