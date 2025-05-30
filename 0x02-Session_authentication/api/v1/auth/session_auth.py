#!/usr/bin/env python3
"""Session Authentication module
"""

import uuid
from typing import Dict, TypeVar

from api.v1.auth.auth import Auth
from models.user import User


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

    def current_user(self, request=None) -> TypeVar('User'):
        """Gets the current user based on a cookie value
        """
        if not request:
            return None
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Deletes the user session (logout)
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]
        return True
