class Chat:
    def __init__(self):
        self.messages = []

    def add_message(self, sender, message):
        self.messages.append(f"{sender}: {message}")

    def get_messages(self, limit=10):
        return self.messages[-limit:]
