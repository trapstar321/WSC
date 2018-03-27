from utils.logging import ConsoleLogger

logger = ConsoleLogger('protocols/client/tcp/protocol.py')

class Protocol(object):
    def on_connected(self):
        logger.info('Connected')

    def on_disconnected(self):
        logger.info('Disconnected')

    def on_message(self, message):
        logger.info('Received => {}'.format(message))

    def send(self, message):
        logger.info('Send => {}'.format(message))