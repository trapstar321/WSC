from protocols.server.tcp.protocol import Protocol

class EchoProtocol(Protocol):
    def on_connected(self, address):
        super(EchoProtocol,self).on_connected(address)

    def on_disconnected(self, address):
        super(EchoProtocol, self).on_disconnected(address)

    def on_message(self, address, message):
        super(EchoProtocol, self).on_message(address, message)
        self.send(address, message)
        #forward message to websocketserver
        self.server.d_b_connector.on_device_message(address, message.decode('utf-8'))

    def send(self, address, message):
        super(EchoProtocol, self).send(address, message)
        self.server.send(address, message)