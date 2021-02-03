from bot.session import Session


class SessionManager:
    def __init__(self, users):
        self.users = users
        self.sessions = {}

    def _create_session(self):
        return Session(self.users)

    def get_session(self, _id):
        if _id not in self.sessions:
            self.sessions[_id] = self._create_session()

        return self.sessions[_id]
