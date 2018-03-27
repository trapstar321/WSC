from protocols.client.websocket.protocol import Protocol
import time

class EchoProtocol(Protocol):
    def on_connected(self):
        super(EchoProtocol, self).on_connected()
        self.send('Hi')

    def on_disconnected(self):
        super(EchoProtocol,self).on_disconnected()

    def on_message(self, message):
        super(EchoProtocol, self).on_message(message)
        self.send(message)
        time.sleep(1)

    def send(self, message):
        super(EchoProtocol, self).send(message)
        self.client.send(message)