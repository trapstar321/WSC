from protocols.server.websocket.protocol import Protocol

class EchoProtocol(Protocol):
    def on_connected(self, address):
        super(EchoProtocol,self).on_connected(address)

    def on_disconnected(self, address):
        super(EchoProtocol, self).on_disconnected(address)

    def on_message(self, address, message):
        super(EchoProtocol, self).on_message(address, message)
        self.send(address, message)

    def send(self, address, message):
        super(EchoProtocol, self).send(address, message)
        self.server.send(address, message)
