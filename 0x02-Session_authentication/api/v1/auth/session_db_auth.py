#!/usr/bin/env python3
""" Session authentication with DB storage
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from models import storage


class SessionDBAuth(SessionExpAuth):
    """Session authentication using database storage
    """

    def create_session(self, user_id: = None) -> str:
        """Create and persist a new session
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(
                user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve user_id based on session_id from DB
        """
        if session_id is None:
            return None
        sessions = storage.search(UserSession)
        for session in sessions:
            if session.session_id == session_id:
                return session.user_id
        return None

    def destroy_session(self, request=None) -> bool:
        """Deletes user session from DB
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        sessions = storage.search(UserSession)
        for session in sessions:
            if session.session_id == session_id:
                storage.delete(session)
                return True
        return False
