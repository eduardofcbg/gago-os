from collections import defaultdict

from bot.session import Session


class SessionManager:
    def __init__(self, users):
        self.users = users
        self.sessions = defaultdict(self._create_session)

    def _create_session(self):
        return Session(self.users)

    def get_session(self, _id):
        return self.sessions[_id]
