class Protocol(object):
    def __init__(self):
        self.clients = []

    def on_connected(self, address):
        self.clients.append(address)

    def on_disconnected(self, address):
        self.clients.remove(address)

    def on_message(self, address, message, headers):
        pass

    def send(self, address, message):
        pass