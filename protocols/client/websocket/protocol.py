class Protocol(object):
    def on_connected(self):
        pass

    def on_disconnected(self):
        pass

    def on_message(self, message):
        pass

    def send(self, message):
        pass