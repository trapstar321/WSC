from protocols.client.websocket.protocol import Protocol
from utils.logging import ConsoleLogger
import time

logger = ConsoleLogger('protocols/client/websocket/echo_protocol.py')


class EchoProtocol(Protocol):
    def on_connected(self):
        super(EchoProtocol, self).on_connected()
        logger.info('Connected')
        self.send('Hi')

    def on_disconnected(self):
        super(EchoProtocol,self).on_disconnected()
        logger.info('Disconnected')

    def on_message(self, message):
        super(EchoProtocol, self).on_message(message)
        logger.info('Received => {}'.format(message))
        self.send(message)
        time.sleep(1)

    def send(self, message):
        super(EchoProtocol, self).send(message)
        logger.info('Send => {}'.format(message))
        self.client.send(message)