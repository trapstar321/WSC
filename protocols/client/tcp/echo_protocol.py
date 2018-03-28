from protocols.client.tcp.protocol import Protocol
from utils.logging import ConsoleLogger
import time

logger = ConsoleLogger('protocols/client/tcp/echo_protocol.py')

class EchoProtocol(Protocol):
    def on_connected(self):
        super(EchoProtocol, self).on_connected()
        logger.info('Connected')
        self.client.send('Hi\n'.encode('utf-8'))

    def on_disconnected(self):
        super(EchoProtocol, self).on_disconnected()
        logger.info('Disconnected')

    def on_message(self, message):
        super(EchoProtocol, self).on_message(message)
        logger.info('Received => {}'.format(message))

        self.send(message)
        time.sleep(3)

    def send(self, message):
        super(EchoProtocol, self).send(message)
        logger.info('Send => {}'.format(message))
        self.client.send(message)