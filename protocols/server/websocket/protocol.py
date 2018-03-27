from utils.logging import ConsoleLogger

logger = ConsoleLogger('protocols/server/websocket/protocol.py')

class Protocol(object):
    def __init__(self):
        self.clients = []

    def on_connected(self, address):
        logger.info('Client {} connected'.format(address))
        self.clients.append(address)

    def on_disconnected(self, address):
        logger.info('Client {} disconnected'.format(address))
        self.clients.remove(address)

    def on_message(self, address, message):
        logger.info('Received message {} from client {}'.format(message, address))

    def send(self, address, message):
        logger.info('Send message {} to client {}'.format(message, address))