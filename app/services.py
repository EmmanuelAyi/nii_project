# In-memory session store
session_store = {}

class Session:
    def __init__(self, session_id):
        self.session_id = session_id
        self.data = session_store.get(session_id, {'stage': '0'})  # Default stage: 0

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    def save(self):
        session_store[self.session_id] = self.data

    def clear(self):
        if self.session_id in session_store:
            del session_store[self.session_id]
