from protocols.server.websocket.protocol import Protocol
from utils.logging import ConsoleLogger

logger = ConsoleLogger('protocols/server/websocket/echo_protocol.py')


class EchoProtocol(Protocol):
    def on_connected(self, address):
        super(EchoProtocol,self).on_connected(address)
        logger.info('Client {} connected'.format(address))

    def on_disconnected(self, address):
        super(EchoProtocol, self).on_disconnected(address)
        logger.info('Client {} disconnected'.format(address))

    def on_message(self, address, message):
        super(EchoProtocol, self).on_message(address, message)
        logger.info('Received message {} from client {}'.format(message, address))
        self.send(address, message)

    def send(self, address, message):
        super(EchoProtocol, self).send(address, message)
        logger.info('Send message {} to client {}'.format(message, address))
        self.server.send(address, message)
